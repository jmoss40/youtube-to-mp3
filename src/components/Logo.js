import icon from '../amber-icon.png';

function Logo(){
  return <div id="toggle_wrapper">
    <span id="logo_background" width="100px" height="100px"><img id="logo" src={icon} alt="Amber Logo" width="100px"/></span>
    <h2 id="logo_text" className="light">Amber's YouTube-to-MP3 Converter</h2>
  </div>
}

export default Logo;