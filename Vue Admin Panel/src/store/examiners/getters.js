export default {
  examiners(state) {
    return state.examiners;
  },
  hasExaminers(state) {
    return state.examiners && state.examiners.length > 0;
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
