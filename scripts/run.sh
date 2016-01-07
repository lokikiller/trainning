#! /bin/sh

### BEGIN INIT INFO
# Provides:          trainning
# Required-Start:
# Required-Stop:
# Should-Start:
# Should-Stop:
# Default-Start:
# Default-Stop:
# Short-Description: Provide service to run trainning
# Description: Control agent and other background service
### END INIT INFO

Module="$2"

module_start() {
  case "$1" in
    agent)
        python ../code/data/kafkaProducer.py
        python ../code/data/kafkaConsumer.py
        ;;
    server)
        python ../code/data/server.py
        ;;
    router)
        python ../code/router.py
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart|reload|status} MODULE\n"
        echo "MODULES:\n"
        echo "agent,  server, router"
        exit 1 
  esac
}

case "$1" in
  start)
        module_start $Module
        ;;
  stop)
        exit 0
        ;;
  status)
        ;;
  restart)
        exit 0
        ;;
  reload)
	exit 0
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|status} MODULE\n"
        exit 1
esac
exit 0
