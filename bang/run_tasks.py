import time
import sys
import os
import subprocess

try:
	import django
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bang.settings")
	django.setup()

	from dag.models import DAG, DAGProcess

	if len(sys.argv) > 1:
		q=sys.argv[1]
		print('Running queue for {}'.format(q))
	else:
		q = None
		print('Running all tasks')

	dag_obj = DAG.objects.get(dag_hash=q)
	dag_process, created = DAGProcess.objects.get_or_create(dag=dag_obj)
	if created:
		pass
	else:
		os.system("taskkill /f /t /pid {}".format(dag_process.pid))
		time.sleep(2)

	while True:
		try:
			time.sleep(2)
			dag_process.refresh_from_db()
			print(dag_process)
			dag_process.pid = os.getpid()
			dag_process.save()
			
			if q is not None:
				run_statement =f'python manage.py process_tasks --queue={q}'
			else:
				run_statement = 'python manage.py process_tasks'
			print(run_statement)
			
			os.system(run_statement)
		except Exception as e:
			print("Error in processing tasks", str(e))

except Exception as e:

	print(f"Exception within run tasks {str(e)}")

time.sleep(10)