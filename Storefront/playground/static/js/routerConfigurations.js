
async function ShowRouters(){
    const data= localStorage.getItem("routerData");
    if(!data){
        console.log("No Data stored");
        return;
    }
    const routers=JSON.parse(data);
    console.log(routers);
    const router_list=document.getElementById("table-body");
    router_list.innerHTML='';
    router_list.innerHTML=routers.map(r=>`
        <tr>
            <td><input type="checkbox" class="tableCheck" id=${r.id} value="${r.id}"></td>
            <td><label for="${r.id}">${r.device}</label></td>
        </tr>
        `).join('');
    const ospfResponse = await fetch(`/playground/ospf-data/`);
    const ospf_data = await ospfResponse.json();    
    document.getElementById("ospf-neighbors").innerHTML
    =`${ospf_data.neighborInfo}`;
    document.getElementById("ospf-database").innerHTML
    =`${ospf_data.databaseInfo}`;
    handleSelectRouters();
}

function HostName(router){
    const host_content=document.getElementById("form-groups");
    host_content.innerHTML='';
    host_content.innerHTML=`
    <div class="form-group">
    <label for="hostname">Host Name:</label>
    <input type="text" id="hostname" name="hostname" placeholder="Enter new host name"> 
    </div>
    <input type="hidden" name="router" value="${router}"> 
    <button type="submit" class="btn">Apply Configuration</button>
    `
    const form=document.getElementById('config-form');
    form.action="/playground/sethostname/";

}
function Banner(router){
    const banner_content=document.getElementById("form-groups");
    banner_content.innerHTML='';
    banner_content.innerHTML=
    `
    <div class="form-group">
    <label for="banner">Banner:</label>     
    <input type="text" id="banner" name="banner" placeholder="Enter new banner">         
    </div>
    <input type="hidden" name="router" value="${router}">      
    <button type="submit" class="btn">Apply Configuration</button>
    `
    const form=document.getElementById('config-form');
    form.action="/playground/setbanner/";
}

function interfaceOptions(selectedDeviceId,type="checkbox") {
    const data = localStorage.getItem('routerData');
    if (!data) {
        console.error('No data found in localStorage.');
        return ;
    }
    const routersData = JSON.parse(data);
    const selected_router = routersData.find(d => d.id === selectedDeviceId);
    console.log(selected_router.interfaces);
    const options = selected_router.interfaces.map(intf => `
            <input type="${type}" id="${intf.name}" name="interfaces" value="${intf.name}">
            <label for="${intf.name}">${intf.name}(${intf.address_subnet})</label>
    `).join('');
    console.log(options);
    return options;
}

function Interface_IP(router){
    const form_content=document.getElementById("form-groups");
    form_content.innerHTML='';
    form_content.innerHTML=
    `
    <div class="form-group">
    <label for="ipv4">IPv4:</label>
    <input type="text" id="ipv4" name="ipv4" placeholder="Enter IPv4 (ip/subnet)" required>
    <div>

    <div class="form-group">
        <label>Interfaces</label>
        <div id="interface-check-container" class="check-group">
        ${interfaceOptions(router,"radio")}
        </div>
    </div>
    
    <input type="hidden" name="router" value="${router}">
    <button type="submit" class="btn">Apply Configuration</button>
    `
    const form=document.getElementById('config-form');
    form.action="/playground/setInterfaceIP/";
}
function Static_Routing(router){
    const form_content=document.getElementById("form-groups");
    form_content.innerHTML='';
    form_content.innerHTML=`
    <input type="hidden" name="router" value="${router}">
    <input type="hidden" id="tag" name="tag" value="add_configration">
    <div class="form-group">
        <label for="cidr">CIDR (Comma-separated)</label>
        <input type="text" id="cidr" name ="cidr" required>
    </div>
    <div class="form-group">
        <label for="next-hop">Next Hop</label>
        <input type="text" id="next-hop" name="next-hop" required>
    </div>
    <div class="form-group">
        <label for="admin-distance">Admin Distance</label>
        <input type="number" id="admin-distance" name="admin-dist" required>
    </div>
    <button type="submit" class="btn">Apply Configuration</button>
    <button type="action" id="delete" class="btn delete">Delete Configuration</button>
    `
    const form=document.getElementById('config-form');
    form.action="/playground/staticrouting/";
    document.getElementById("delete").addEventListener("click", ()=> 
        {
            document.getElementById("tag").value = "remove_configration";
        });
}

function ospf(router){
    const form_content=document.getElementById("form-groups");
    form_content.innerHTML='';
    form_content.innerHTML=`
        <input type="hidden" name="routers" value="${router}">
        <input type="hidden" id="tag" name="tag" value="add_configration">

        <div class="form-group">
            <label for="cidr">CIDR (Comma-separated)</label>
            <input type="text" id="cidr" name ="cidr" required>
        </div>
        <div class="form-group">
            <label for="ospf-id">OSPF ID</label>
            <input type="text" id="ospf-id" name ="ospf-id" required>
        </div>
        <div class="form-group">
            <label for="area-id">Area ID</label>
            <input type="text" id="area-id" name="area-id" required>
        </div>
        <div class="form-group">
            <label for="router-id">Router ID</label>
            <input type="text" id="router-id" name="router-id" required>
        </div>
        <div class="form-group">
            <label>Interfaces</label>
            <div id="interface-check-container" class="check-group">    
                ${interfaceOptions(router)}
            </div>
        </div>
        <div class="form-group">
            <label for="hello-timer">Hello Timer</label>
            <input type="number" id="hell-timer" name="hello-timer" required>
        </div>
        <div class="form-group">
            <label for="dead-timer">Dead Timer</label>
            <input type="number" id="dead-timer" name="dead-timer" required>
        </div>
        <button type="submit" class="btn">Apply Configuration</button>
        <button type="action" id="delete"class="btn delete">Delete Configuration</button>   
        `;
    
    const form=document.getElementById('config-form');
    form.action="/playground/ospf/";
    document.getElementById("delete").addEventListener("click", ()=> 
        {
            document.getElementById("tag").value = "remove_configration";
        });

}
function OneRouterSelected(router){
    const tab_buttons=document.getElementById("tab-buttons");
    tab_buttons.innerHTML='';
    tab_buttons.innerHTML=`
    <button id="host-tab" class="tab">Set Host Name</button>
    <button id="banner-tab" class="tab">Set Banner</button>
    <button id="interface-tab" class="tab">Set Interface IP</button>
    <button id ="static-tab" class="tab">Static Routing</button> 
    <button id="ospf-tab" class="tab">OSPF Configuration</button>
    `;
    const host_tab=document.getElementById("host-tab");
    host_tab.addEventListener('click',()=>{
        HostName(router);
        const active=document.getElementsByClassName("active")[0]?.classList.remove("active");
        host_tab.classList.add("active");
    });
    const banner_tab=document.getElementById("banner-tab");
    banner_tab.addEventListener('click',()=>{
        Banner(router);
        document.getElementsByClassName("active")[0]?.classList.remove("active");
        banner_tab.classList.add("active");
    });
    const interface_tab= document.getElementById("interface-tab");
    interface_tab.addEventListener('click',()=>{
        Interface_IP(router);
        document.getElementsByClassName("active")[0]?.classList.remove("active");
        interface_tab.classList.add("active")
    });
    const static_tab=document.getElementById("static-tab")
    static_tab.addEventListener('click',()=>{
        Static_Routing(router);
        document.getElementsByClassName("active")[0]?.classList.remove("active");
        static_tab.classList.add("active");
    });
    const ospf_tab=document.getElementById("ospf-tab");
    ospf_tab.addEventListener('click',()=>{
        ospf(router);
        document.getElementsByClassName("active")[0]?.classList.remove("active");
        ospf_tab.classList.add("active");
    });
}

function ManyRouterSelected(selected){
    const tab_buttons=document.getElementById("tab-buttons");
    tab_buttons.innerHTML='';
    tab_buttons.innerHTML=`
    <button id="ospf-tab" class="active">OSPF Configuration</button>
    `;
    const form_content=document.getElementById("form-groups");
    form_content.innerHTML='';
    form_content.innerHTML=`
        <input type="hidden" name="routers" value="${selected}">
        <input type="hidden" id="tag" name="tag" value="add_configration">
        <div class="form-group">
            <label for="area-id">Area ID</label>
            <input type="text" id="area-id" name="area-id" required>
        </div>
        <div class="form-group">
            <label for="hello-timer">Hello Timer</label>
            <input type="number" id="hell-timer" name="hello-timer" required>
        </div>
        <div class="form-group">
            <label for="dead-timer">Dead Timer</label>
            <input type="number" id="dead-timer" name="dead-timer" required>
        </div>
        <button type="submit" class="btn">Apply Configuration</button>
        <button type="action" id="delete"class="btn delete">Delete Configuration</button>
        `;
    const form=document.getElementById('config-form');
    form.action="/playground/ospf/";
    document.getElementById("delete").addEventListener("click", ()=> 
        {
            document.getElementById("tag").value = "remove_configration";
        });
    
}
function handleSelectRouters(){
    let checkboxs = document.querySelectorAll("input.tableCheck");
    console.log(checkboxs);
    checkboxs.forEach(check=>{
        check.addEventListener('change',async ()=>{
            
            document.getElementById("form-groups").innerHTML='';
            const selected=document.querySelectorAll("input.tableCheck:checked");
            if(selected.length===0){
                document.getElementById("tab-buttons").innerHTML='';
            }else if(selected.length===1){
                OneRouterSelected(selected[0].value);
            }else{
                const routers=Array.from(selected).map(x=>x.value);
                ManyRouterSelected(routers);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    await ShowRouters();
    setInterval(ShowRouters, 600000);  // Refresh every 600,000 milliseconds (10 minutes)
});
