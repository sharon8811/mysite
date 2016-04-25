from fabric.api import local, run, env, cd, prefix

from fabric.colors import green, red


def prepare():
    #local("./manage.py test polls")
    local("git add -p && git commit")
    local("git push")


def mysite():

    env.hosts = ['13.80.16.72']

    env.use_ssh_config = True




def deploy_quick_no_restart():



    path = "/home/ironscales/irons"

    process = "Deploy Quick No REstart"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')



    print(red("DONE!"))



def deploy_quick():



    path = "/home/ironscales/irons"

    process = "Deploy Quick"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')



        print(green("Restart the server and workers processes"))

        run('./scripts/restart_server.sh')

    print(red("DONE!"))



def deploy_quick_all():



    path = "/home/ironscales/irons"

    process = "Deploy Quick"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')



        print(green("Restart the server and workers processes"))

        run('./scripts/restart_all.sh')

    print(red("DONE!"))



def deploy_quick_all_statics():



    path = "/home/ironscales/irons"

    process = "Deploy Quick With Statics"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')

        with prefix('source ./scripts/set_env.sh'):

            master = run("echo $MASTER")

            if master == "True":

                print(green("Collecting static files..."))

                run('./manage.py collectstatic')



        print(green("Restart the server and workers processes"))

        run('./scripts/restart_all.sh')

    print(red("DONE!"))



def deploy_db():



    path = "/home/ironscales/irons"

    process = "Deploy With Migrate DB"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')

        with prefix('source ./scripts/set_env.sh'):

            master = run("echo $MASTER")

            if master == "True":

                print(green("Collecting static files..."))

                run('./manage.py collectstatic')

                print(green("Syncing the database..."))

                run('./manage.py migrate')



        print(green("Restart the server and workers processes"))

        run('./scripts/restart_all.sh')

    print(red("DONE!"))



def deploy_db_no_statics():



    path = "/home/ironscales/irons"

    process = "Deploy With Migrate DB No Statics"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')

        with prefix('source ./scripts/set_env.sh'):

            master = run("echo $MASTER")

            if master == "True":

                print(green("Syncing the database..."))

                run('./manage.py migrate')



        print(green("Restart the server and workers processes"))

        run('./scripts/restart_all.sh')

    print(red("DONE!"))



def deploy_full():



    path = "/home/ironscales/irons"

    process = "Deploy Full"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')

        print(green("Run upgrade.sh script"))



        with prefix('source ./scripts/set_env.sh'):

            try:

                run('./scripts/upgrade.sh')

            except:

                pass



            master = run("echo $MASTER")

            if master == "True":

                print(green("Collecting static files..."))

                run('./manage.py collectstatic')

                print(green("Syncing the database..."))

                run('./manage.py migrate')



        print(green("Restart the server and workers processes"))

        run('./scripts/reload_config.sh')

    print(red("DONE!"))





def reload_config():



    path = "/home/ironscales/irons"

    process = "Reload config files"



    print(red(process))

    with cd(path) :

        with prefix('source ./scripts/set_env.sh'):

            try:

                print(green("Reloading files..."))

                run('./scripts/reload_config.sh')

                print(green("Reload succeed!"))

            except:

                print(red("Reload failed!"))

                pass



    print(red("DONE!"))