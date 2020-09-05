from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

handle = open('/tmp/dependency1.out', 'a')

handle.write(date + "\n")

handle.close()
