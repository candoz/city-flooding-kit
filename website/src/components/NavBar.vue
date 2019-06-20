<template>
    <div>
      <nav>
        <li style="float:left"> City Flooding Kit </li>
        <li> About </li>
        <li> Administrator Area </li>
        <!-- <router-link tag="li" :to="'/'" exact>Explore</router-link>
        <router-link tag="li" :to="'/write'" exact>Write</router-link>
        <router-link tag="li" v-if="logged === false" :to="'/login'" exact>Login</router-link>
        <router-link tag="li" v-if="logged === false" :to="'/signup'" exact>Signup</router-link>
        <router-link tag="li" v-if="logged === true" :to="'/profile'" exact>MyProfile</router-link> -->
      </nav>
    </div>
</template>

<script>
export default {
  props: ["logged"],
  data() {
    return {
      
    };
  },
};
</script>

<style scoped>
nav {
  /* top: 0;
  left: 0;
  width: 100%;
  background-color: #393939;
  position: fixed;
  display: flex;
  flex-wrap: nowrap;
  list-style: none;
  justify-content: right;
  z-index: 1;
  overflow-x: auto; */

  position: fixed;
  top: 0;
  width: 100%;
  /* list-style-type: none; */
  margin: 10;
  padding: 0px 12px;
  overflow: hidden;
  background-color: #333;
}
nav li {
  /* border-radius: 4px 4px 0px 0px;
  flex: 1;
  max-width: 75px;
  
  text-decoration: none;
  font-size: 110%; */
  display: block;
  color: white;
  text-align: center;
  padding: 12px 12px;
  margin: 0px;
  text-decoration: none;
  float: right;
}
nav li.router-link-active :not(:hover) {
  background-color: #14a76c;
  cursor: pointer;
}
nav li:hover {
  background-color: #202020;
  cursor: pointer;
}
</style>
