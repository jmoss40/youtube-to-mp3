import {useEffect, useState} from "react";

function DarkModeToggle() {
  const [toggleDark, setToggleDark] = useState(false);
  
  var changeHandler = () => {
    localStorage.setItem("toggleDark", !toggleDark);
    setToggleDark(!toggleDark);
  }
  
  let theme = localStorage.getItem("toggleDark");
  if(!theme){
    localStorage.setItem("toggleDark", false);
    setToggleDark(false);
  }else if(toggleDark !== (theme === 'true')){
    setToggleDark(!toggleDark);
  }
  
  useEffect(()=>{
    let mode = toggleDark?"dark":"light"
    document.body.className = mode;
    document.getElementById("logo_text").className = mode;
    document.getElementById("darkmode_label").className = mode;
  }, [toggleDark, setToggleDark]);

  return (
    <div id="toggle_wrapper">
      <label name="toggle" className="switch">
        <input type="checkbox" onChange={changeHandler}/>
        <span className="slider round"></span>
        <div className="light" id="darkmode_label">Dark Mode</div>
      </label>
    </div>
  )
}

export default DarkModeToggle;
