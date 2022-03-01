import { Component } from "react";
import Logo from './Logo.js';
import icon from '../download-icon.png'
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import '../../node_modules/react-toastify/dist/ReactToastify.css';

class Converter extends Component {
  constructor(props){
    super(props);
    this.state = {
      url : ""
    }
    this.changeHandler = this.changeHandler.bind(this);
    this.submitHandler = this.submitHandler.bind(this);
  }

  changeHandler = (e) => {
    this.setState({[e.target.name]: e.target.value});
  }
 
  submitHandler = (e) => {
    e.preventDefault();
    var type = e.target.name;
    var {url} = this.state;

    if(type === "") type = "mp3"; //set a default type to handle errors
    let data = {
      "type": type,
      "url": url
    }
    
    toast.dark("Thanks! Your download is on the way.");
    
    axios.post("http://localhost:5000/download", data, {
      responseType: 'arraybuffer'
    }).then((res)=>{
      let filename = res.headers["content-disposition"].substring(21);
      let blob;
      if(url.match(/playlist/))
        blob = new Blob([res.data], { type: 'application/zip' })
      else
        blob = new Blob([res.data], { type: 'audio/mp3' })

      const downloadUrl = URL.createObjectURL(blob)
      let a = document.createElement("a"); 
      a.href = downloadUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
    }).catch((error)=>{
      toast.error("Error: Something went wrong. Please try again.");
      console.log(error);
    });
  }

  render() {
    var {url} = this.state;
    return(
      <div id="content">
        <ToastContainer position="top-left" autoClose={3000} pauseOnFocusLoss={false}/>
        <Logo/>
        <input id="url_field" autoComplete="off" size={100} name="url" placeholder="Enter the YouTube video or playlist's url here..." value={url} type="url" onChange={this.changeHandler}/>
        <button type="button" className="download_button" name="mp3" onClick={this.submitHandler}><img src={icon} width={15}/>MP3</button>
        <button type="button" className="download_button" name="mp4" onClick={this.submitHandler}><img src={icon} width={15}/>MP4</button> 
      </div>
    );
  }
}

export default Converter;
  