﻿var settings = {
  "liveOnly": true,
  "command": "!steal",
  "permission": "Everyone",
  "minAmount": 10,
  "maxAmount": 10000,
  "chance": 50,
  "useCooldown": true,
  "useCooldownMessages": true,
  "cooldown": 30,
  "onCooldown": "$user, $command is still on global cooldown for $cd minutes!",
  "userCooldown": 180,
  "onUserCooldown": "$user, $command is still on user cooldown for $cd minutes!",
  "responseWon": "$user stole $stealAmount $currency from $victim.",
  "responseLost": "$user couldn't steal any $currency and lost $stealAmount $currency to $victim.",
  "responsePointsNotInRange": "$user the amount for stealing needs to be between $minAmount and $maxAmount $currency.",
  "responseNotEnoughPoints": "$user, you need $stealAmount $currency to steal. It might go sideways!"
};