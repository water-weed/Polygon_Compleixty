import { createStore } from 'vuex';

const store = createStore({
  state: {
    details: null, // store details data
  },
  mutations: {
    // set details data
    setDetails(state, payload) {
      state.details = payload;
    },
  },
  actions: {
    // asynchronously set details
    async setDetailsAsync({ commit }, payload) {
      // simulate asynchronous operations
      const processedDetails = await new Promise((resolve) => {
        setTimeout(() => resolve(payload), 1000);
      });
      commit('setDetails', processedDetails);
    },
  },
  getters: {
    // get details values
    getDetails: (state) => state.details,
  },
});

export default store;
