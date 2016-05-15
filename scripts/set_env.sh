config_file="./conf/mysite.conf"

if [ ! -f $config_file ]; then
	echo "Please copy the right config file to conf/ironscales.conf"
	exit
fi

source $config_file 

export LOGGING_LEVEL=$logging_level

export DEPLOYMENT=${deployment^^}

if [ -z $hostname ]; then
	export HOSTNAME=https://365testdomain.com
else
	export HOSTNAME=$hostname
fi

export EMAIL_HOST=$smtp_server
export EMAIL_PORT=$smtp_port

export EMAIL_HOST_USER=$smtp_user
export EMAIL_HOST_PASSWORD=$smtp_pass

if [ -z $smtp_tls ]; then
	export USE_TLS=False
elif [ $smtp_tls == "true" ]; then
	export USE_TLS=True
else
	export USE_TLS=False
fi

if [ $master == "true" ]; then
	export MASTER=True
else
	export MASTER=False
fi

