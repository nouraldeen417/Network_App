function switch_tabs(tab){
    document.getElementsByClassName('active')[0]?.classList.remove('active');
    document.getElementById(tab).classList.add('active');
    document.getElementsByClassName('active-section')[0]?.classList.add('non-active-section');
    document.getElementsByClassName('active-section')[0]?.classList.remove('active-section');
    document.getElementsByClassName(tab)[0]?.classList.remove('non-active-section');
    document.getElementsByClassName(tab)[0]?.classList.add('active-section');
    populateDevices(tab);
}
document.addEventListener('DOMContentLoaded',function(){
    console.log('hello');
    Array.from(document.getElementsByClassName('tab-btn')).forEach(e=>{
        e.addEventListener('click',()=>switch_tabs(e.id));
    });
    let upload_box=document.getElementById('upload-box');
    let file_input=document.getElementById('file-input');
    console.log(upload_box);
    console.log(file_input);
    upload_box.addEventListener('click',()=>file_input.click());
    file_input.addEventListener('change',()=>{
        console.log('change');
        if(file_input.files.length>0){
            upload_box.textContent=`Selected: ${file_input.files[0].name}`;
        }
    });
    upload_box.addEventListener('dragover',(e)=>{
        e.preventDefault();
        console.log('drapover');
        upload_box.classList.add('highlight');
    });
    upload_box.addEventListener('dragleave',()=>{
        console.log('dragleave');
        upload_box.classList.remove('highlight');
    });
    upload_box.addEventListener('drop',(e)=>{
        e.preventDefault();
        console.log('drop');
        upload_box.classList.remove('highlight');
        if(e.dataTransfer.files.length){
            file_input.files=e.dataTransfer.files;
            upload_box.textContent=`Selected: ${file_input.files[0].name}`;
        }
    });
    
    document.getElementById('add-device-form').addEventListener('submit',async (e)=>{
        e.preventDefault();
        let url="/playground/add_device/";
        await sendRequest(url,e);
    });
    
    document.getElementById('upload-form').addEventListener('submit',async (e)=>{
        e.preventDefault();
        let url='/playground/upload-file/'
        await sendRequest(url,e);
    });
    document.getElementById('paste-form').addEventListener('submit',async (e)=>{
        e.preventDefault();
        let url='/playground/paste-config/'
        await sendRequest(url,e);
    });
    document.getElementById('backup-form').addEventListener('submit',async (e)=>{
        e.preventDefault();
        let url='/playground/backup/'
        await sendRequest(url,e);
    });
    
    
});
let x=0;
async function sendRequest(url,e){
    let formData=new FormData(e.target);
        let response=await fetch(url,{
            method:'POST',
            body:formData
        });
        let data = await response.json();
        console.log(data);
        await e.target.reset();
        let result_box=document.getElementById('result-box');
        result_box.innerHTML=data.response;
        if(data.response=='ok'){
            result_box.classList.remove('error');
            result_box.classList.add('success');
        }else {
            result_box.classList.remove('success');
            result_box.classList.add('error');
        }
}

function populateDevices(tab){
    const data=sessionStorage.getItem('devices');
    const devices=JSON.parse(data);
    const table_body=document.querySelector(`#device-table-${tab} tbody`);
    table_body.innerHTML='';
    devices.forEach(d=>{
        let row=document.createElement('tr');
        let radio=document.createElement('input');
        radio.type=(tab=='backup')?'checkbox':'radio';
        radio.name='device';
        radio.value=d.host;
        let cell=document.createElement('td');
        cell.appendChild(radio)
        row.appendChild(cell);
        Object.values(d).forEach(p=>{
            cell=document.createElement('td');
            cell.appendChild(document.createTextNode(p));
            row.appendChild(cell);
        });
        row.style.cursor='pointer';
        row.onclick=()=>radio.checked=!radio.checked;
        table_body.appendChild(row);
    });

}