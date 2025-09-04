// src/services/api.js
import axios from "axios";

// Базовый URL к твоему NestJS API
const api = axios.create({
  baseURL: "http://localhost:3000/api", // ⚡ здесь твой backend
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  // 1. Получение конкурса по id
  async getPrize(id) {
    const { data } = await api.get(`/prizes/${id}`);
    return data;
  },

  // 2. Получение всех пользователей конкурса
  async getUsersByPrize(id) {
    const { data } = await api.get(`/prizes/${id}/users`);
    return data;
  },

  // 3. Добавление пользователя в конкурс
  async addUserToPrize(prizeId, telegram_id, username) {
    const { data } = await api.post(`/prizes/${prizeId}/users`, {
      telegram_id,
      username,
    });
    return data;
  },

  // 4. Удаление пользователя из конкурса
  async removeUserFromPrize(prizeId, telegram_id) {
    await api.delete(`/prizes/${prizeId}/users/${telegram_id}`);
    return true;
  },

  // 5. Обновление конкурса (например, isFinished)
  async updatePrize(prizeId, payload) {
    const { data } = await api.patch(`/prizes/${prizeId}`, payload);
    return data;
  },
};
