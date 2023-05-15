<template>
  <div>
    <input
      v-model="search"
      type="text"
      class="form-control"
      placeholder="Search..."
    />

    <table class="table">
      <thead>
        <tr>
          <th v-for="(value, key) in items[0]" :key="key">
            {{ key }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in filteredItems" :key="item.id">
          <td v-for="value in item" :key="value">
            {{ value }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
      search: '',
    };
  },

  computed: {
    filteredItems() {
      return this.items.filter((item) => {
        return Object.values(item).some((value) =>
          value.toString().toLowerCase().includes(this.search.toLowerCase())
        );
      });
    },
  },

  async created() {
  try {
    const response = await axios.get('https://repeaters.seve-ai.com/data', {
      headers: {
        'X-API-Key': '643cd615b54b64e48a3fb8545de2d44c379d9798ba86e08c7b5559519dc050f3',
      },
    });
    this.items = response.data;
  } catch (error) {
    console.error(error);
  }
},


};
</script>
