<!-- 643cd615b54b64e48a3fb8545de2d44c379d9798ba86e08c7b5559519dc050f3
  https://repeaters.seve-ai.com/data
 -->
 <template>
  <div>
    <div class="search-bar">
      <input v-model="search" type="text" placeholder="Search..."/>
    </div>
    <div class="table-container">
    <table>
      <thead>
        <tr>
          <th v-for="(value, key) in items[0]" :key="key">
            {{ key }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in filteredItems" :key="index">
          <td v-for="(value, key) in item" :key="key">
            {{ value }}
          </td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const items = ref([]);
    const search = ref('');

    const fetchData = async () => {
      try {
        const response = await axios.get('https://repeaters.seve-ai.com/data', {
          headers: {
            'X-API-Key': '643cd615b54b64e48a3fb8545de2d44c379d9798ba86e08c7b5559519dc050f3'
          }
        })
        items.value = response.data.data;
      } catch (error) {
        console.error(error)
      }
    }

    const filteredItems = computed(() => {
      if (search.value === '') {
        return items.value;
      }

      return items.value.filter(item => 
        Object.values(item).some(val => 
          val?.toString().toLowerCase().includes(search.value.toLowerCase())
        )
      )
    });

    onMounted(fetchData);

    return { items, search, filteredItems };
  }
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
}

.search-bar {
  position: sticky;
  top: 0;
  left: 0;
  width: 30%;
  padding: 10px;
  background-color: #f9f9f9;
  z-index: 100;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.table-container {
  margin-top: 5px; /* adjust this value based on the height of your search bar */
  height: 600px;
  overflow-y: scroll;
  padding: 20px;
}

input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border-radius: 4px;
  border: 1px solid #ccc;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
}

input:focus {
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}

table {
  width: 90%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  padding: 12px 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

tr:hover {
  background-color: #ddd;
  transition: background-color 0.3s ease;
}
</style>
