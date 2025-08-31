<template>
  <div :class="style.header__timer">
    <!-- Часы -->
    <div :class="style.header__timer_time">
      <div :class="style.header__timer_block">{{ hoursTens }}</div>
      <div :class="style.header__timer_block">{{ hoursOnes }}</div>
    </div>
    <div :class="style.header__timer_division">:</div>

    <!-- Минуты -->
    <div :class="style.header__timer_time">
      <div :class="style.header__timer_block">{{ minutesTens }}</div>
      <div :class="style.header__timer_block">{{ minutesOnes }}</div>
    </div>
    <div :class="style.header__timer_division">:</div>

    <!-- Секунды -->
    <div :class="style.header__timer_time">
      <div :class="style.header__timer_block">{{ secondsTens }}</div>
      <div :class="style.header__timer_block">{{ secondsOnes }}</div>
    </div>
  </div>
</template>

<script>
import style from "../PrizePageComponent.module.scss";

export default {
  name: "Timer",
  props: {
    // длительность таймера в секундах
    duration: {
      type: Number,
      default: 1200, // 3 часа
    },
  },
  data() {
    return {
      totalSeconds: this.duration,
      timerInterval: null,
      style,
    };
  },
  computed: {
    hours() {
      return Math.floor(this.totalSeconds / 3600);
    },
    minutes() {
      return Math.floor((this.totalSeconds % 3600) / 60);
    },
    seconds() {
      return this.totalSeconds % 60;
    },
    hoursTens() {
      return Math.floor(this.hours / 10);
    },
    hoursOnes() {
      return this.hours % 10;
    },
    minutesTens() {
      return Math.floor(this.minutes / 10);
    },
    minutesOnes() {
      return this.minutes % 10;
    },
    secondsTens() {
      return Math.floor(this.seconds / 10);
    },
    secondsOnes() {
      return this.seconds % 10;
    },
  },
  mounted() {
    this.timerInterval = setInterval(() => {
      if (this.totalSeconds > 0) {
        this.totalSeconds--;
      } else {
        clearInterval(this.timerInterval);
      }
    }, 1000);
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  },
};
</script>
