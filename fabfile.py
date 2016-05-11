from fabric.api import local, run, env, cd, prefix

from fabric.colors import green, red


def prepare():
    local('python manage.py test')

    try:
        local('git commit -a')
    except:
        pass
    #local('git push origin master')
    local('git checkout master && git pull && git merge --no-ff dev')
    local('git push origin master')
    #local('git checkout dev')



def azure():
    env.hosts = ['13.80.16.72']
    env.use_ssh_config = True








def deploy():



    path = "/home/sharon/mysite"

    process = "Deploy Quick"



    print(red("Beginning Deploy:"))

    with cd(path) :

        print(green("Pulling master from origin..."))

        run('git pull')



        print(green("Done pulling new version"))

        #run('./scripts/restart_server.sh')

    print(red("DONE!"))