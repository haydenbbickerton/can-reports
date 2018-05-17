<template>
  <div class="app-container">
    <el-card class="box-card">
      <article class="markdown-body">
        <vue-markdown :source="text_data" :watches="['text_data']"></vue-markdown>
      </article>
    </el-card>
  </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'
import 'github-markdown-css/github-markdown.css'

export default {
  components: {
    'vue-markdown': VueMarkdown
  },
  mounted () {
    fetch('https://rawgit.com/haydenbbickerton/2b88fff2058da22c2c098389109cf9a8/raw/8c3bf7f3e05f05f2333debf4cd75bdabdd12b5a2/notes.md')
    .then((response) => {
      return response.text();
    })
    .then((myText) => {
      this.text_data = myText
    });
  },
  data() {
    return {
      text_data: "",
    }
  },
}
</script>

<style>
.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 45px;
}

@media (max-width: 767px) {
  .markdown-body {
    padding: 15px;
  }
}
</style>
