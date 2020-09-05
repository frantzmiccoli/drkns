from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

handle = open('/tmp/project2.out', 'w')

handle.write(date)

handle.close()
