from appadmin.models import ProcessPackages

import pkgutil
from pip._internal.operations.freeze import freeze
import sys


def update_dependencies():
    ## Imported / Installed Packages
    package_list = [{'package_name' :  x.split('==')[0]
                        ,'import_name' :  x.split('==')[0]
                        ,'current_version' :  x.split('==')[1]} for x in freeze()]
    
    for package in package_list:
        pp, created = ProcessPackages.objects.get_or_create(
            package_name=package['package_name']
        )
        if created:
            pp.import_name = package['import_name']
        pp.current_version = package['current_version']
        pp.save()
        print(package, created)

    ## Default Packages
    for default_package in pkgutil.iter_modules():
        if not default_package.name.startswith('_'):
            pp, created = ProcessPackages.objects.get_or_create(
                package_name=default_package.name
            )
            if created:
                pp.import_name = default_package.name
            pp.current_version = None
            pp.is_base_package = True
            pp.save()
            print(default_package, created)

    ## Sys Packages
    for sys_package in sys.builtin_module_names:
        if not sys_package.startswith('_'):
            pp, created = ProcessPackages.objects.get_or_create(
                package_name=sys_package
            )
            if created:
                pp.import_name = sys_package
            pp.current_version = None
            pp.is_base_package = True
            pp.save()
            print(sys_package, created)