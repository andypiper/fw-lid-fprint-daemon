#!/usr/bin/env bash
# laptop-lid-daemon.sh — persistent poller for lid+externals → fprintd toggle

prev_state=""
while true; do
  # Read lid state
  STATE=$(awk '{print $2}' /proc/acpi/button/lid/LID0/state 2>/dev/null)
  docked=0
  if [[ "$STATE" == closed ]]; then
    for conn in /sys/class/drm/*-DP-*/status /sys/class/drm/*-HDMI-A-*/status; do
      [[ -e $conn ]] || continue
      if grep -q connected "$conn"; then
        docked=1
        break
      fi
    done
  fi

  # Determine state key
  if [[ "$STATE" == open ]]; then
    key="open"
  elif (( docked )); then
    key="closed-docked"
  else
    key="closed-undocked"
  fi

  # Act on changes only
  if [[ "$key" != "$prev_state" ]]; then
    case "$key" in
      open)
        logger -t lid-daemon "LID OPEN → unmask & start fprintd"
        systemctl unmask fprintd.service
        systemctl start  fprintd.service
        ;;
      closed-docked)
        logger -t lid-daemon "LID CLOSED + DOCKED → mask & stop fprintd"
        systemctl stop  fprintd.service
        systemctl mask fprintd.service
        ;;
      closed-undocked)
        logger -t lid-daemon "LID CLOSED + UNDOCKED → leave fprintd alone"
        ;;
    esac
    prev_state="$key"
  fi

  sleep 15
done
