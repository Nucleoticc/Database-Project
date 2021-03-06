<template>
  <table class="table">
    <thead>
      <tr>
        <th v-for="header in headers" :key="header">{{header}}</th>
      </tr>
      <tr v-for="row in data" :key="row.id">
        <td v-for="rd in row" :key="rd">{{rd}}</td>
        <button v-if="row.status=='Pending'" class="button is-danger is-light" @click="setActive(row.id)" >Activate</button>
      </tr>
    </thead>
  </table>
</template>

<script>
export default {
  props: ['headers', 'data'],
  methods: {
    async setActive(id){
      await this.$store.dispatch('categories/activateCategory', {
        'id':id
      })
    }
  }
};
</script>

<style scoped>
table {
  display: flex;
  justify-content: center;
  text-align: center;
}

</style>
