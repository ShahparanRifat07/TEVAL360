//Sidebar dropdown
const allDropdown = document.querySelectorAll("#sidebar .side-dropdown");
const sidebar = document.getElementById("sidebar");

allDropdown.forEach((item) => {
  const a = item.parentElement.querySelector("a:first-child");
  a.addEventListener("click", function (e) {
    e.preventDefault();

    if (!this.classList.contains("active")) {
      allDropdown.forEach((i) => {
        const aLink = i.parentElement.querySelector("a:first-child");

        aLink.classList.remove("active");
        i.classList.remove("show");
      });
    }

    this.classList.toggle("active");
    item.classList.toggle("show");
  });
});

//SIDEBAR COLLAPSE

const toggleSidebar = document.querySelector("nav .toggle-sidebar");

toggleSidebar.addEventListener("click", function () {
  sidebar.classList.toggle("hide");
});

sidebar.addEventListener("mouseleave", function () {
  if (this.classList.contains("hide")) {
    allDropdown.forEach((item) => {
      const a = item.parentElement.querySelector("a:first-child");
      a.classList.remove("active");
      item.classList.remove("show");
    });
  }
});

sidebar.addEventListener("mouseenter", function () {
  if (this.classList.contains("hide")) {
    allDropdown.forEach((item) => {
      const a = item.parentElement.querySelector("a:first-child");
      a.classList.remove("active");
      item.classList.remove("show");
    });
  }
});

//Profile dropdown

const profile = document.querySelector("nav .profile");
const imgProfile = profile.querySelector("img");
const dropdownProfile = profile.querySelector(".profile-link");

imgProfile.addEventListener("click", function () {
  dropdownProfile.classList.toggle("show");
});

window.addEventListener("click", function (e) {
  if (e.target !== imgProfile) {
    if (e.target != dropdownProfile) {
      if (dropdownProfile.classList.contains("show")) {
        dropdownProfile.classList.remove("show");
      }
    }
  }
});

//Chart Demos > Pie Charts > Simple Pie
//chart-1
var options = {
  series: [
    {
      data: [4.3, 4.2, 3.9, 4.7, 1.2, 2.4],
    },
  ],
  chart: {
    type: "bar",
    height: 380,
  },
  plotOptions: {
    bar: {
      barHeight: "100%",
      distributed: true,
      horizontal: true,
      dataLabels: {
        position: "bottom",
      },
    },
  },
  colors: [
    "#33b2df",
    "#546E7A",
    "#d4526e",
    "#13d8aa",
    "#A5978B",
    "#2b908f",
    "#f9a3a4",
    "#90ee7e",
    "#f48024",
    "#69d2e7",
  ],
  dataLabels: {
    enabled: true,
    textAnchor: "start",
    style: {
      colors: ["#000"],
    },
    formatter: function (val, opt) {
      return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val;
    },
    offsetX: 0,
    dropShadow: {
      enabled: true,
    },
  },
  stroke: {
    width: 1,
    colors: ["#fff"],
  },
  xaxis: {
    categories: [
      "Classroom Interaction",
      "Assessment",
      "Counseling & Mentoring",
      "Research & Development",
      "Organizational Qualities",
      "Administrative skills",
    ],
  },
  yaxis: {
    labels: {
      show: false,
    },
  },
  title: {
    text: "Rating Associate with Category",
    align: "center",
    floating: true,
  },
  subtitle: {
    text: "Evaluation-2023",
    align: "center",
  },
  tooltip: {
    theme: "dark",
    x: {
      show: false,
    },
    y: {
      title: {
        formatter: function () {
          return "";
        },
      },
    },
  },
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

//chart-2

var options = {
  series: [
    {
      name: "Rating",
      data: [4.2, 3.1, 4.2, 4.4, 3.9],
    },
  ],
  chart: {
    height: 350,
    type: "line",
    zoom: {
      enabled: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "straight",
  },
  title: {
    text: "Overall Rating Summary",
    align: "center",
  },
  subtitle: {
    text: "Per Evaluation",
    align: "center",
  },
  grid: {
    row: {
      colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
      opacity: 0.5,
    },
  },
  xaxis: {
    categories: ["2018", "2019", "2020", "2021", "2022"],
  },
  yaxis: {
    title: {
      text: "Rating",
    },
    min: 0,
    max: 5,
  },
};

var chart = new ApexCharts(document.querySelector("#chart1"), options);
chart.render();

//chart-3
var options = {
  series: [
    {
      data: [4.3, 4.2, 3.9, 4.7, 4.0, 3.7],
    },
  ],
  chart: {
    type: "bar",
    height: 380,
  },
  plotOptions: {
    bar: {
      barHeight: "100%",
      distributed: true,
      horizontal: false,
      dataLabels: {
        position: "top",
      },
    },
  },
  colors: [
    "#33b2df",
    "#546E7A",
    "#d4526e",
    "#13d8aa",
    "#A5978B",
    "#2b908f",
    "#f9a3a4",
    "#90ee7e",
    "#f48024",
    "#69d2e7",
  ],
  dataLabels: {
    enabled: true,
    textAnchor: "center",
    style: {
      colors: ["#000"],
    },
    formatter: function (val, opt) {
      return val;
    },
    offsetX: 0,
    dropShadow: {
      enabled: true,
    },
  },
  stroke: {
    width: 1,
    colors: ["#fff"],
  },
  xaxis: {
    categories: [
      "English-I (A)",
      "English-I (B)",
      "English-II (A)",
      "English-II (A)",
      "Math (B)",
      "Bangla (C)",
    ],
  },
  yaxis: {
    labels: {
      show: false,
    },
  },
  title: {
    text: "Rating Associate with Course",
    align: "center",
    floating: true,
  },
  subtitle: {
    text: "Evaluation-2023",
    align: "center",
  },
  tooltip: {
    theme: "dark",
    x: {
      show: false,
    },
    y: {
      title: {
        formatter: function () {
          return "";
        },
      },
    },
  },
};

var chart = new ApexCharts(document.querySelector("#chart2"), options);
chart.render();














//admin dashboard

var options = {
  series: [76, 90, 61, 90, 60],
  chart: {
    height: 400,
    type: "radialBar",
  },
  plotOptions: {
    radialBar: {
      offsetY: 0,
      startAngle: 0,
      endAngle: 270,
      hollow: {
        margin: 5,
        size: "30%",
        background: "transparent",
        image: undefined,
      },
      dataLabels: {
        name: {
          show: false,
        },
        value: {
          show: false,
        },
      },
    },
  },
  title: {
    text: "Evaluation Completed Percentage (2023)",
    align: "center",
    floating: true,
  },
  colors: ["#33b2df",
    "#546E7A",
    "#d4526e",
    "#13d8aa",
    "#A5978B",
    "#2b908f",
    "#f9a3a4",
    "#90ee7e",
    "#f48024",
    "#69d2e7",],

  labels: ["Student", "Teacher", "Parent", "Administrator", "Self"],
  legend: {
    show: true,
    floating: true,
    fontSize: "12px",
    position: "left",
    offsetX: 160,
    offsetY: 15,
    labels: {
      useSeriesColors: true,
    },
    markers: {
      size: 0,
    },
    formatter: function (seriesName, opts) {
      return seriesName + ":  " + opts.w.globals.series[opts.seriesIndex] + "%";
    },
    itemMargin: {
      vertical: 3,
    },
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        legend: {
          show: false,
        },
      },
    },
  ],
};

var chart = new ApexCharts(document.querySelector("#chart-admin-1"), options);
chart.render();



var options = {
  series: [220, 18, 110, 7],
  chart: {
    height: 350,
    type: 'pie',
  },
  title: {
    text: "Total User Percentages",
    align: "left",
    floating: true,
  },
  labels: ['Student', 'Teacher', 'Parent', 'Administrator'],
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
};

var chart = new ApexCharts(document.querySelector("#chart-admin-2"), options);
chart.render();






//Create Evaluation
$('#datepicker').daterangepicker({
  locale: {
           format: 'DD/MM/YYYY'
           }
});

$(function () {
  var dtToday = new Date();

  var month = dtToday.getMonth() + 1;
  var day = dtToday.getDate();
  var year = dtToday.getFullYear();
  if (month < 10) month = "0" + month.toString();
  if (day < 10) day = "0" + day.toString();

  var maxDate = year + "-" + month + "-" + day;
  // alert(maxDate);
  $("#start_date").attr("min", maxDate);
  $("#end_date").attr("min", maxDate);

  $("#start_date").on("change", function () {
    $("#end_date").attr("min", $(this).val());
  });

  $("#end_date").on("change", function () {
    $("#start_date").attr("max", $(this).val());
  });
});

const studentCheckbox = document.querySelector("#stakeholder-student");
const studentFactors = document.querySelector(".student-factors");

studentCheckbox.addEventListener("click", function () {
  studentFactors.classList.toggle("evaluation-form-div-show");
});

const teacherCheckbox = document.querySelector("#stakeholder-teacher");
const teacherFactors = document.querySelector(".teacher-factors");

teacherCheckbox.addEventListener("click", function () {
  teacherFactors.classList.toggle("evaluation-form-div-show");
});

const parentCheckbox = document.querySelector("#stakeholder-parent");
const parentFactors = document.querySelector(".parent-factors");

parentCheckbox.addEventListener("click", function () {
  parentFactors.classList.toggle("evaluation-form-div-show");
});

const selfCheckbox = document.querySelector("#stakeholder-self");
const selfFactors = document.querySelector(".self-factors");

selfCheckbox.addEventListener("click", function () {
  selfFactors.classList.toggle("evaluation-form-div-show");
});

const administratorCheckbox = document.querySelector(
  "#stakeholder-adminstrator"
);
const administratorFactors = document.querySelector(".adminstrator-factors");

administratorCheckbox.addEventListener("click", function () {
  administratorFactors.classList.toggle("evaluation-form-div-show");
});

$(document).ready(function () {
  $(":checkbox:checked").prop("checked", false);
});

//add student using excel
// $(function () {
//   function formatBytes(a, b) {
//     if (0 == a) return "0 Bytes";
//     var c = 1024,
//       d = b || 2,
//       e = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"],
//       f = Math.floor(Math.log(a) / Math.log(c));
//     return parseFloat((a / Math.pow(c, f)).toFixed(d)) + " " + e[f];
//   }

//   $("#dropzone").on("dragover", function () {
//     $(this).addClass("dragover");
//   });

//   $("#dropzone").on("dragleave", function () {
//     $(this).removeClass("dragover");
//   });
//   $("#dropzone input").on("change", function (e) {
//     $("#dropzone").removeClass("dragover");
//     var file = this.files[0],
//       fileExt,
//       fileType,
//       keepFile;
//     if ($(file).length === 0) {
//       var ext = "Drag your file to upload";
//     } else if (
//       ~file.type.lastIndexOf("xlsx") ||
//       ~file.type.lastIndexOf("xls")
//     ) {
//       const basicTruncate = (str, strLgth = 19) => {
//         const truncStr = str.substring(0, strLgth);
//         return str.length > strLgth ? `${truncStr}...${fileExt}` : str;
//       };
//       var fileExt = file.name.split(".").pop(),
//         fileType = fileExt == "xlsx" ? "xlsx" : "xlsx",
//         fileName = "<div class=fileok>" + basicTruncate(file.name) + "</div>",
//         open_in =
//           '<svg style="width:24px;height:24px" viewBox="0 0 24 24"><path fill="#000000" d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/></svg>',
//         icon = "<div class=" + fileType + ">" + fileExt + "</div>",
//         fileSize = "<div class=filesize>[" + formatBytes(file.size) + "]</div>";
//       ext = icon + "<div>" + fileName + fileSize + "</div>";
//     } else {
//       var ext = "Invalid file format";
//       e.target.value = "";
//     }
//     $("#dropzone div").html(ext);
//     // if (~file.type.indexOf('image')) {
//     //   var reader = new FileReader(file);
//     //   reader.readAsDataURL(file);
//     //   // reader.onload = function(e) {
//     //   //   var data = e.target.result,
//     //   //       $img = $('<img />').attr('src', data).fadeIn();
//     //   //   $('#dropzone div').html($img);
//     //   // };
//     // }
//   });
// });

