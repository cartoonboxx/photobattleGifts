<template v-if="prizeData">
  <header :class="style.header">
    <div :class="style.header__upper">
      <div :class="style.header__upper__stars">
        <img src="@/images/star.png" alt="star" />
        <h1>{{ prizeData.prize_size }}</h1>
      </div>
      <div :class="style.triangle"></div>
    </div>

    <picture :class="style.header__picture">
      <source srcset="@/images/gift.webp" type="image/webp" />
      <img src="@/images/gift.png" />
    </picture>
    <div>
      <h1 :class="style.header__text">Раздача Telegram Stars</h1>
      <p>
        {{ prizeData.winners_count }} призов по
        {{ prizeData.prize_size }} Telegram Stars
      </p>
      <Timer />
      <p>
        Будьте онлайн на этой странице в,<br />чтобы принять участие в раздаче
      </p>
    </div>
  </header>
  <main :class="style.main">
    <h3>Участников онлайн: {{ users.length }}</h3>
    <span>Ваша позиция:</span>
    <p>Приглашайте друзей, чтобы увеличить шансы</p>
    <UserCard />
    <h2>Топ 10 лидеров</h2>
    <UserList :users="users" />
    <div :class="style.inviteWrapper">
      <a href="https://google.com" :class="style.invite_users"
        >Пригласить друзей</a
      >
    </div>
  </main>
</template>

<script lang="ts">
import style from "./PrizePageComponent.module.scss";
import Timer from "@/page/prize/components/Timer.vue";
import { defineComponent } from "vue";
import UserCard from "@/page/prize/components/UserCard/UserCard.vue";
import UserList from "@/page/prize/components/UserList/UserList.vue";
import http from "@/httpService";
import { PrizeObj } from "@/page/prize/prize.types";

export default defineComponent({
  components: { UserList, UserCard, Timer },
  data() {
    return {
      prizeData: {} as PrizeObj,
      users: [],
      currentUserInfo: {},
      style,
      http,
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    // console.log(this.prizeData);
    console.log(window?.Telegram?.WebApp?.initData);
    this.prizeData = await http.getPrize(id);
    this.users = await http.getUsersByPrize(id);
    console.log(this.prizeData);
  },
});
</script>
