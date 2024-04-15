<template>
  <el-tag
    v-text="val[0] + '/' + value.name"
    style="margin-right: 10px; margin-top: 5px"
    :title="value.name"
    :color="value.color"
    effect="dark"
    type="info"
  ></el-tag>
</template>

<script>
var tp = [
  {
    name: "name",
    expression: /^nr/i,
    color: "#50c6fb",
  },
  {
    name: "place",
    expression: /^ns/i,
    color: "#d07f7f",
  },
  {
    name: "organization",
    expression: /^nt/i,
    color: "#8e8b8b",
  },
  {
    name: "string",
    expression: /^nx/i,
    color: "#96dbf8",
  },
  {
    name: "proper noun",
    expression: /^nz/i,
    color: "#8bc3f5",
  },
  {
    name: "noun",
    expression: /^n/i,
    color: "#488fce",
  },
  {
    name: "phone number",
    expression: /^tel/i,
    color: "#999",
  },
  {
    name: "time word",
    expression: /^t/i,
    color: "#c7aee7",
  },
  {
    name: "处所词",
    expression: /^s/i,
    color: "#cee887",
  },
  {
    name: "方位词",
    expression: /^f/i,
    color: "#c9aaca",
  },
  {
    name: "verb",
    expression: /^v/i,
    color: "#ffcb99",
  },
  {
    name: "adjective",
    expression: /^a/i,
    color: "#67ccaa",
  },
  {
    name: "区别词",
    expression: /^b/i,
    color: "#67a6d9",
  },
  {
    name: "status word",
    expression: /^z/i,
    color: "#f3e988",
  },
  {
    name: "pronoun",
    expression: /^r/i,
    color: "#9acccd",
  },
  {
    name: "numeral",
    expression: /^m/i,
    color: "#986699",
  },
  {
    name: "quantifier",
    expression: /^q/i,
    color: "#ff9899",
  },
  {
    name: "adverb",
    expression: /^d/i,
    color: "#ffcccb",
  },
  {
    name: "preposition",
    expression: /^p/i,
    color: "#99cc67",
  },
  {
    name: "conjunction",
    expression: /^c/i,
    color: "#8ea4de",
  },
  {
    name: "Web links",
    expression: /^url/i,
    color: "#999",
  },
  {
    name: "particle",
    expression: /^u/i,
    color: "#4dd9e6",
  },
  {
    name: "e-mail",
    expression: /^email/i,
    color: "#999",
  },
  {
    name: "interjection",
    expression: /^e/i,
    color: "#d7acd7",
  },
  {
    name: "modal",
    expression: /^y/i,
    color: "#f48363",
  },
  {
    name: "onomatopoeia",
    expression: /^o/i,
    color: "#f2d404",
  },
  {
    name: "prefix",
    expression: /^h/i,
    color: "#30aadd",
  },
  {
    name: "ID number",
    expression: /^id/i,
    color: "#999",
  },
  {
    name: "IP address",
    expression: /^ip/i,
    color: "#999",
  },
  {
    name: "suffix",
    expression: /^k/i,
    color: "#999",
  },
  {
    name: "punctuation",
    expression: /^w/i,
    color: "#999",
  },
];
export default {
  props: ["val"],
  computed: {
    value() {
      for (let i of tp) {
        if (i.expression.test(this.val[1])) {
          return i;
        }
      }
    },
  },
};
</script>