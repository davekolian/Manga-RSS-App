import React from "react";

const div_bg_css = {
  height: "500px",
  width: "250px",
  backgroundColor: "green",
};

function Manga() {
  return (
    <div style={div_bg_css}>
      <h1>Manga1</h1>
      <img
        src="https://avt.mkklcdnv6temp.com/20/b/16-1583494192.jpg"
        alt="bg"
      />
    </div>
  );
}

export default Manga;
