import os

from flask import Flask, request, render_template


app = Flask(__name__)


######################################root#############################################

@app.route('/')
def index():
    return render_template('index.html')


################################## FTP Configure #######################################

@app.route('/ftp.html', methods=['POST', 'GET'])
def ftp_fun():
    if request.method == 'POST':
        if request.form['submit'] == 'FTP Start':
            os.system("dnf -y install vsftpd")
            os.system("systemctl restart vsftpd")
            os.system("systemctl enable vsftpd")
            os.system("firewall-cmd --permanent --add-port=21/tcp")
            os.system("firewall-cmd --reload")
            return "<script> alert('FTP configured');  window.location = 'ftp.html';</script>"
        elif request.form['submit'] == 'FTP Stop':
            os.system("/sbin/service vsftpd stop")
            return "<script> alert('FTP service Stop');  window.location = 'ftp.html';</script>"
        elif request.form['submit'] == 'Upload File':
            ftp_file = request.form['ftp_file']
            ftp_upload_cmd = "cp " + ftp_file + " /var/ftp/pub/cfg_files/"
            os.system(ftp_upload_cmd)
            os.system("restorecon /var/ftp/pub/cfg_files/*")
            return "<script> alert('File Uploaded on FTP server'); window.location = 'ftp.html';</script>"
        return render_template('ftp.html')
    elif request.method == 'GET':
        return render_template('ftp.html')



############################################################################################

if __name__ == '__main__':
    app.run(debug=True)

