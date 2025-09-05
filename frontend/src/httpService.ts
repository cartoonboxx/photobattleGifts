import axios from "axios";

const api = axios.create({
  baseURL: "http://giveawaystars.ru/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  async getPrize(id) {
    const { data } = await api.get(`/prizes/${id}`);
    return data;
  },

  async getUsersByPrize(id) {
    const { data } = await api.get(`/prizes/${id}/users`);
    return data;
  },

  async addUserToPrize(prizeId, telegram_id, username) {
    const { data } = await api.post(`/prizes/${prizeId}/users`, {
      telegram_id,
      username,
    });
    return data;
  },

  async removeUserFromPrize(prizeId, telegram_id) {
    await api.delete(`/prizes/${prizeId}/users/${telegram_id}`);
    return true;
  },

  async updatePrize(prizeId, payload) {
    const { data } = await api.patch(`/prizes/${prizeId}`, payload);
    return data;
  },
};
