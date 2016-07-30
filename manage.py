from flask.ext.script import Manager
from packages.app import app
from packages.objects import Package
from packages.kpack import PackageInfo
from packages.config import _cfg
from packages.database import db

import os

manager = Manager(app)

@manager.command
def calc_package_file_sizes():
    packages = Package.query.all()
    for package in packages:
        path = build_package_path(package)
        size = PackageInfo.get_file_size(path)
        package.file_size = size
    
    db.commit()
    return None
    # update db

def build_package_path(p):
    return os.path.join(_cfg("storage"), p.repo, "{0}-{1}.pkg".format(p.name, p.version))

if __name__ == "__main__":
    manager.run() 
