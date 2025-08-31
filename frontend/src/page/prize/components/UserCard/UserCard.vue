<template>
  <div :class="style.userCard">
    <img src="" alt="" />
    <div :class="style.userInfo">
      <h1>Jasbin</h1>
      <p>
        <img src="@/images/chance.svg" alt="" />
        7.21% шанс
      </p>
    </div>
    <p>78 <img src="@/images/user-ico.png" /></p>
  </div>
</template>

<script>
import style from "./UserCard.module.scss";

export default {
  name: "UserCard",
  data() {
    return {
      style,
    };
  },
};
</script>
