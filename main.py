import subprocess
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

report_filename = "report-result.html"
class AmarthaSecurityTool:
    def __init__(self):
        #Check prerequisites
        prerequisites = subprocess.run("""
        steampipe --version &&
        powerpipe --version
        """, shell=True, capture_output=True, text=True)
        if prerequisites.returncode != 0:
            # Print the error checking
            sys.stderr.write("\033[91m An error occurred when checking the prerequisites: {0} \033[0m \n".format(prerequisites.stderr))
            sys.exit()

    def cloud_scan(self):
        # Shell command to execute
        scan_command = "powerpipe benchmark run amartha_compliance --export={0}".format(report_filename)

        # Execute the command
        result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)
        print("Scan output:")
        print(result.stdout)

    def send_email(self):
        # Email configuration
        smtp_server = "smtp.mailtrap.io"
        smtp_port = 2525
        sender_email = "security-tools@amartha.com"
        receiver_email = "engineer@amartha.com"
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Security Report"

        # Read the HTML file
        with open(report_filename, 'r') as file:
            html_content = file.read()

        # Add body to the email
        html_report = MIMEText(html_content, 'html')
        message.attach(html_report)

        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection

        # Send email
        text = message.as_string()
        server.login("fdbe363e464a39", "20121b2b9fbecc")
        server.sendmail(sender_email, receiver_email, text)
        # Close the connection
        server.quit()

        print("Email sent!")
        

def main():
    # Create instance
    tooling_script = AmarthaSecurityTool()
    # Scan cloud environment
    tooling_script.cloud_scan()
    # Sending report via email
    tooling_script.send_email()

if __name__ == "__main__":
    main()

