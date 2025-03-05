function ShowSwitches(){
    const data= localStorage.getItem("switchData");
    console.log("before");
    console.log(data);
    if(!data){
        console.log("No Data stored");
        return;
    }
    const switches=JSON.parse(data);
    console.log(switches);
    const switch_list=document.getElementById("table-body");
    switch_list.innerHTML='';
    switch_list.innerHTML=switches.map(r=>`
        <tr>
            <td><input type="checkbox" class="tableCheck" id=${r.id} value="${r.id}"></td>
            <td><label for="${r.id}">${r.device}</label></td>
        </tr>
        `).join('');
    handleSelectSwitches();
}

function HostName(device){
    const host_content=document.getElementById("form-groups");
    host_content.innerHTML='';
    host_content.innerHTML=`
    <div class="form-group">
    <label for="hostname">Host Name:</label>
    <input type="text" id="hostname" name="hostname" placeholder="Enter new host name" required> 
    </div>
    <input type="hidden" name="switch" value="${device}"> 
    <button type="submit" class="btn">Apply Configuration</button>
    `
    const form=document.getElementById('config-form');
    form.action="/playground/sethostname/";

}
function Banner(device){
    const banner_content=document.getElementById("form-groups");
    banner_content.innerHTML='';
    banner_content.innerHTML=
    `
    <div class="form-group">
    <label for="banner">Banner:</label>     
    <input type="text" id="banner" name="banner" placeholder="Enter new banner" required>         
    </div>
    <input type="hidden" name="switch" value="${device}">      
    <button type="submit" class="btn">Apply Configuration</button>
    `
    const form=document.getElementById('config-form');
    form.action="/playground/setbanner/";
}

function interfaceOptions(selectedDeviceId,type="checkbox") {
    const data = localStorage.getItem('switchData');
    if (!data) {
        console.error('No data found in localStorage.');
        return ;
    }
    const switchesData = JSON.parse(data);
    const selected_switch = switchesData.find(d => d.id === selectedDeviceId);
    console.log(selected_switch.interfaces);
    const options = selected_switch.interfaces.map(intf => `
            <input type="${type}" id="${intf.name}" name="interfaces" value="${intf.name}">
            <label for="${intf.name}">${intf.name}(${intf.address_subnet})</label>
    `).join('');
    console.log(options);
    return options;
}

function gateway(device){
    const form_content=document.getElementById("form-groups");
    form_content.innerHTML='';
    form_content.innerHTML=
    `
    <div class="form-group">
    <label for="gateway">Gateway:</label>     
    <input type="text" id="gateway" name="gateway" placeholder="Enter Gateway" required>         
    </div>

    <div class="form-group">
            <label>Interfaces</label>
            <div id="interface-check-container" class="check-group">
            ${interfaceOptions(device,'radio')}
            </div>
        </div>

    <input type="hidden" name="switch" value="${device}">      
    <button type="submit" class="btn">Apply Configuration</button>
    `;
    const form=document.getElementById('config-form');
    form.action="/playground/gateway/";
}
async function vlan(selectedDeviceId) {
    console.log("Fetching VLAN brief from URL...");
    const reponse = await fetch(`/playground/vlan-brief/`);
    const vlanBrief = await reponse.json();
    console.log(vlanBrief.vlan);
    let configBody = document.getElementById("form-groups");
    configBody.innerHTML = '';
    configBody.innerHTML = `
        <div class="form-group">
            <label for="vlan-id">VLAN ID</label>
            <input type="number" id="vlan-id" name="vlan-id" placeholder="Enter VLAN ID (1-4094)" min="1" max="4094" required">
        </div>
        <div class="form-group">
            <label for="vlan-name" required>VLAN Name</label>
            <input type="text" id="vlan-name" name="vlan-name" placeholder="Enter VLAN Name" required>
        </div>
        <div class="form-group">
            <label>Interfaces</label>
            <div id="interface-check-container" class="check-group">
            ${interfaceOptions(selectedDeviceId)}
            </div>
        </div>
        <div class="form-group">
            <label for="vlan-cidr" >VLAN CIDR</label>
            <input type="text" id="vlan-cidr" name="vlan-cidr" required>
        </div>
        <input type="hidden" id="switches" name="switches" value=${[selectedDeviceId]}>
        <input type="hidden" id="tag" name="tag" value="add_configration">
        <button type="submit" class="btn">Apply Configuration</button>
        <button type="action" id="delete"class="btn delete">Delete Configuration</button>
        <div class="command-output">
            <h2>VLAN Brief Information</h2>
            <textarea name="vlan-brief" id="vlan-brief" readonly>
                ${vlanBrief.vlan}
            </textarea>
            <h2>VLAN Detailed Information</h2>
            <textarea name="vlan-detail" id="vlan-detail" readonly>

            </textarea>
        </div>
        `;
    const form = document.getElementById('config-form');
    form.action = "/playground/vlan/";
    document.getElementById("delete").addEventListener("click", () => {
        document.getElementById("tag").value = "remove_configration";
    });
}
function OneSwitchSelected(device){
    const tab_buttons=document.getElementById("tab-buttons");
    tab_buttons.innerHTML='';
    tab_buttons.innerHTML=`
    <button id="host-tab">Set Host Name</button>
    <button id="banner-tab">Set Banner</button>
    <button id="gateway-tab">Switch gateway</button>
    <button id="vlan-tab">Vlan Configuration</button>
    `;  
    const host_tab=document.getElementById("host-tab");
    host_tab.addEventListener('click',()=>{
        HostName(device);
        const active=document.getElementsByClassName("active")[0]?.classList.remove("active");
        host_tab.classList.add("active");
    });
    const banner_tab=document.getElementById("banner-tab");
    banner_tab.addEventListener('click',()=>{
        Banner(device);
        document.getElementsByClassName("active")[0]?.classList.remove("active");
        banner_tab.classList.add("active");
    });
    const interface_tab= document.getElementById("gateway-tab");
    interface_tab.addEventListener('click',()=>{
        gateway(device);
        document.getElementsByClassName("active")[0]?.classList.remove("active");
        interface_tab.classList.add("active");
    });
    const vlan_tab=document.getElementById("vlan-tab");
    vlan_tab.addEventListener('click',()=>{
        vlan(device);
        document.getElementsByClassName("active")[0]?.classList.remove("active");
        vlan_tab.classList.add("active");    
    });
    
}
async function ManySwitchSelected(selected){
    console.log("Fetching VLAN brief from URL...");
    const reponse = await fetch(`/playground/vlan-brief/`);
    const vlanBrief = await reponse.json();
    const tab_buttons=document.getElementById("tab-buttons");
    tab_buttons.innerHTML='';
    tab_buttons.innerHTML=`
    <button id="vlan-tab" class="active">Vlan Configuration</button>
    `;
    const configBody = document.getElementById("form-groups");
        configBody.innerHTML = '';
        configBody.innerHTML = `
            <div class="form-group">
                <label for="vlan-id">VLAN ID</label>
                <input type="number" id="vlan-id" name="vlan-id" placeholder="Enter VLAN ID (1-4094)" min="1" max="4094" required">
            </div>
            <div class="form-group">
                <label for="vlan-name">VLAN Name</label>
                <input type="text" id="vlan-name" name="vlan-name" placeholder="Enter VLAN Name" required>
            </div>
            <input type="hidden" id="switches" name="switches" value=${selected}>
            <input type="hidden" id="tag" name="tag" value="add_configration">
            <button type="submit" class="btn">Apply Configuration</button>
            <button type="action" id="delete" class="btn delete">Delete Configuration</button>
            <div class="command-output">
            <h2>VLAN Brief Information</h2>
            <textarea name="vlan-brief" id="vlan-brief" readonly>
                ${vlanBrief.vlan}
            </textarea>
            <h2>VLAN Detailed Information</h2>
            <textarea name="vlan-detail" id="vlan-detail" readonly>
                
            </textarea>
            </div>
            `;
    console.log(configBody.innerHTML);
    const form=document.getElementById('config-form');
    form.action="/playground/vlan/";
    document.getElementById("delete").addEventListener("click", ()=> 
    {
        document.getElementById("tag").value = "remove_configration";
    });
}
function handleSelectSwitches(){
    let checkboxs = document.querySelectorAll("input.tableCheck");
    console.log(checkboxs);
    checkboxs.forEach(check=>{
        check.addEventListener('change',()=>{
            
            document.getElementById("form-groups").innerHTML='';
            const selected=document.querySelectorAll("input.tableCheck:checked");
            if(selected.length===0){
                document.getElementById("tab-buttons").innerHTML='';
            }else if(selected.length===1){
                OneSwitchSelected(selected[0].value);
            }else{
                const routers=Array.from(selected).map(x=>x.value);
                ManySwitchSelected(routers);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    ShowSwitches();
    setInterval(ShowSwitches, 600000);  // Refresh every 600,000 milliseconds (10 minutes)
});
