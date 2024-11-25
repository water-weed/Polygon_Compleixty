import { createStore } from 'vuex';

const store = createStore({
  state: {
    details: null, // 存储复杂的 details 数据
  },
  mutations: {
    // 设置 details 的数据
    setDetails(state, payload) {
      state.details = payload;
    },
  },
  actions: {
    // 异步设置 details（如果需要）
    async setDetailsAsync({ commit }, payload) {
      // 模拟异步操作
      const processedDetails = await new Promise((resolve) => {
        setTimeout(() => resolve(payload), 1000);
      });
      commit('setDetails', processedDetails);
    },
  },
  getters: {
    // 获取 details 数据
    getDetails: (state) => state.details,
  },
});

export default store;
