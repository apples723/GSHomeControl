 #give me all your passwords please 
export HUSER="Qu-NI3EF-U0snB3NrT4qqv36kkFS09VGJyANg37Q"
export HADDR="169.254.11.125"

#date for logs
function hue_log {
  local pre="$(date '+%m%d-%H')"
  local log_dir="${HOME}/.ha/hue/logs/"
  local full_log="${log_dir}${pre}.log"
  rm $full_log > /dev/null
  touch $full_log > /dev/null
  echo $full_log
}

#where we at 

function hue_state { 
  local LIGHT=$1
  local STATE=$(curl -s -X GET http://$HADDR/api/$HUSER/lights/$LIGHT | jq ".state.on") 
  if [ $STATE == "true" ]
  then 
    echo "on"
  else 
    echo "off"
  fi
}

 
#shut it downnnn
function hue_off {
  local LIGHT=$1
  local HLOG=$(hue_log)
  curl -X PUT -d '{"on":false}' http://$HADDR/api/$HUSER/lights/$LIGHT/state &> "$HLOG"
}
#start the partyyy
function hue_on {
  local LIGHT=$1
  local HLOG=$(hue_log)
  curl -X PUT -d '{"on":true}' http://$HADDR/api/$HUSER/lights/$LIGHT/state &> "$HLOG"
}

function hue_brigtness { 
  local LIGHT=$1
  local BRI=$2
  local HLOG_ONCE=$(hue_log)
  local HLOG=$HLOG_ONCE
  if [ -z "$2" ] 
  then 
    echo "use: hue_brightness <light> <brightness_level[0-100]>" 
  fi
  sleep 1
  hue_on $LIGHT
  curl -X PUT -d '{"bri": '${BRI}'}' http://$HADDR/api/$HUSER/lights/$LIGHT/state &> "$HLOG"
} 


