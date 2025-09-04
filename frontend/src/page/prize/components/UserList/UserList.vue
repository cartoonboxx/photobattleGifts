<template>
  <div :class="style.userList">
    <!-- отрисовываем только те, что видимы -->
    <UserCard
      v-for="(user, index) in visibleUsers"
      :key="user.id ?? index"
      :user="user"
      :class="style.userCard"
    />
    <div
      v-if="!showAll && hiddenCount > 0"
      :class="style.showMore"
      @click="showAllUsers"
      role="button"
      :aria-label="`и еще ${hiddenCount} участников`"
    >
      и еще {{ hiddenCount }} участников
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import UserCard from "@/page/prize/components/UserCard/UserCard.vue";
import style from "./UserList.module.scss";

export default defineComponent({
  name: "UserList",
  components: { UserCard },
  props: {
    users: {
      type: Array as PropType<any[]>,
      required: true,
    },
    // опционально: можно изменить число видимых карточек (по умолчанию 2)
    initialVisible: {
      type: Number as PropType<number>,
      default: 10,
    },
  },
  data() {
    return {
      showAll: false,
      style,
    };
  },
  computed: {
    visibleUsers(): any[] {
      return this.showAll
        ? this.users
        : this.users.slice(0, this.initialVisible);
    },
    hiddenCount(): number {
      return this.showAll
        ? 0
        : Math.max(0, this.users.length - this.initialVisible);
    },
  },
  methods: {
    showAllUsers() {
      this.showAll = true;
      // при необходимости можно прокинуть событие наружу:
      // this.$emit('expanded')
    },
  },
});
</script>
