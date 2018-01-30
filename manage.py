#!/usr/bin/env python
import os
from app import create_app, db
from app.models import tblUser, tblRole, Room, Paiju
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

app = create_app(os.getenv('PYTHON_CONFIG') or 'default')
manager = Manager(app)
#  migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, tblUser=tblUser,tblRole=tblRole, Room=Room, Paiju=Paiju)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
# manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()
