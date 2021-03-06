export default {
  students(state) {
    return state.students;
  },
  hasStudents(state) {
    return state.students && state.students.length > 0;
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
