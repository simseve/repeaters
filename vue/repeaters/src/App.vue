<template>
  <section>
    <header>
      <h1>Ponti ripetitori</h1>
    </header>
    <TableRep />
  </section>
</template>

<script>
import TableRep from './components/TableRep.vue'

export default {
  name: 'App',
  components: {
    TableRep
  }
}
</script>

<style>

* {
  box-sizing: border-box;
}
html {
  font-family: 'Jost', sans-serif;
}
body {
  margin: 0;
}
header {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 3rem auto;
  border-radius: 10px;
  padding: 1rem;
  background-color: #58004d;
  color: white;
  text-align: center;
  width: 100%;
  max-width: 80rem;
}

#app h2 {
  font-size: 4rem;
  border-bottom: 4px solid #ccc;
  color: #58004d;
  margin: 0 0 1rem 0;
}

</style>
