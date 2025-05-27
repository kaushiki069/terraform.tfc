from ansible.module_utils.basic import AnsibleModule
import requests
import os

def list_projects(organization):
    url = f"https://app.terraform.io/api/v2/organizations/{organization}/projects"
    headers = {
        "Authorization": f"Bearer {os.getenv('TFC_TOKEN')}",
        "Content-Type": "application/vnd.api+json",
    }

    response = requests.get(url, headers=headers)
    project_names=[]
    
    res=response.json()
    for item in res.get('data', []):
        name = item.get('attributes', {}).get('name')
        if name:
            project_names.append(name)
    if response.status_code != 200:
        raise Exception(f"Failed to list projects: {response.status_code} {response.text}")

    return project_names
def main():
   module = AnsibleModule(
       argument_spec=dict(
           action=dict(type='str', required=False, default="list"),
           organization=dict(type='str', required=True)
       )
   )


   action = module.params['action']
   organization = module.params['organization']
   result = {"changed": False, "action": action}


   try:
       if action == "list":
           output = list_projects(organization)
           result["changed"] = True
           result["message"] = "Projects listed successfully"
           result["output"] = output
       else:
           module.fail_json(msg=f"Invalid action: {action}. Only 'list' is supported.", **result)


       module.exit_json(**result)


   except Exception as e:
       module.fail_json(msg=str(e), **result)


if __name__ == '__main__':
   main()


