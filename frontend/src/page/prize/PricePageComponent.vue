<template>
  <header :class="style.header">
    <div :class="style.header__upper">
      <div :class="style.header__upper__stars">
        <img src="@/images/star.png" alt="star" />
        <h1>gfdgdfhg</h1>
      </div>
      <div :class="style.triangle"></div>
    </div>

    <picture :class="style.header__picture">
      <source srcset="@/images/gift.webp" type="image/webp" />
      <img src="@/images/gift.png" />
    </picture>
    <div>
      <h1 :class="style.header__text">
        Раздача Telegram Stars<br />321 призов по 123 Telegram Stars
      </h1>
      <Timer />
      <p :class="style.header__paragraph">
        Будьте онлайн на этой странице в,<br />чтобы принять участие в раздаче
      </p>
    </div>

    <h1 :class="style.header__text">
      Раздача Telegram Stars<br />Встречайте победителей!
    </h1>
    <p :class="style.header__paragraph">Розыгрыш завершился в</p>
  </header>
  <main :class="style.main">
    <a href="https://google.com" :class="style.invite_users"
      >Пригласить друзей</a
    >
  </main>
</template>

<script>
import style from "./PrizePageComponent.module.css";
import Timer from "@/page/prize/components/Timer.vue";

export default {
  components: { Timer },
  data() {
    return {
      style,
    };
  },
};
</script>
