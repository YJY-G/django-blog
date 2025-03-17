/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html","../templates/*.html"],
  theme: {
    container:{
      center:true,
      screens:{
        md:"1120px",
        lg:"1120px",
        xl:"1120px",
        "2xl":"1120px",
      }
    },
    extend: {
      colors: {
        primary: "#E50046",
        secondary: "#A9B5DF",
        third: "#7886C7",
        fourth: "#2D336B",
        fifth: "#F5EFFF",
        sixth: "#E5D9F2",
        seventh: "#F2E2B1",
        eighth: "#D5C7A3",
        ninth: "#F5EFFF",
        tenth: "#A594F9",
      },
    },
  },
  plugins: [],
}

