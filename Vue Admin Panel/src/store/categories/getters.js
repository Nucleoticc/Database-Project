export default {
  categories(state) {
    return state.categories;
  },
  hasCategories(state) {
    return state.categories && state.categories.length > 0;
  },
  shouldUpdate(state) {
    const lastFetch = state.lastFetch;
    if (!lastFetch) {
      return true;
    }
    const currentTimestamp = new Date().getTime();
    return (currentTimestamp - lastFetch) / 1000 > 60;
  }
};
