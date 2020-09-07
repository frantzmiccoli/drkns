from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

handle = open('/tmp/project1.drknsdemo.out', 'w')

handle.write(date)

handle.close()
