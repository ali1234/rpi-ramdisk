# The following profile fragment makes the terminal
# rows/cols be correct when logging in over serial

resize() {

  old=$(stty -g)
  stty raw -echo min 0 time 5

  printf '\033[18t' > /dev/tty
  IFS=';t' read -r _ rows cols _ < /dev/tty

  stty "$old"

  # echo "cols:\$cols"
  # echo "rows:\$rows"
  stty cols "$cols" rows "$rows"
}

[ $(tty) = /dev/ttyAMA0 ] && resize