<h1>Task Management Module</h1>

<p>This Odoo module, named "task_management", provides functionality for managing tasks with deadlines, collects visitor ip adresses and their locations and views them in the main website page. It introduces a new model called "Task" with various fields for capturing task details. Additionally, there is a "Stages" model that allows categorizing tasks into different stages. The module includes three views: form, list, and calendar, providing different ways to interact with the tasks.</p>

<h2>Features</h2>

<ul>
  <li><strong>IP Address Collection:</strong>The ip address of the device you log with into the odoo webiste will be collected and shown with its information regarding: Country, City, Provider, Timezone, etc..</li>
  <li><strong>Task Model:</strong> The main model of the module is "Task," which includes the following fields:
    <ul>
      <li>Name: The name of the task.</li>
      <li>Description: Additional details or notes about the task.</li>
      <li>Deadline: The deadline or due date for the task.</li>
      <li>Stage: The stage or category of the task, determined by the "Stages" model.</li>
      <li>Creator: The user who created the task record.</li>
    </ul>
  </li>
  <li><strong>Stages Model:</strong> The "Stages" model allows categorizing tasks into different stages. It includes a single field, "Name," to define the name of each stage.</li>
  <li><strong>Security Groups:</strong> The module includes two security groups for the "Task" model, providing controlled access to the task records:
    <ul>
      <li>Own Records: Users belonging to this group can create and update task records. However, they can only view their own records.</li>
      <li>All Records: Users belonging to this group have similar privileges as the "Own Records" group but can access and view all task records created by any user.</li>
    </ul>
  </li>
  <li><strong>Task Report:</strong> The module allows generating a printable report of task records. Users can select the desired tasks and then choose to print the report.</li>
  <li><strong>Website Integration:</strong> Tasks can be accessed through the website menu named "Task Management." Clicking on a specific task in the menu provides detailed information about that task.</li>
</ul>

<h2>Installation</h2>

<ol>
  <li>Download the "task_management" module from the provided source.</li>
  <li>Place the module directory inside the Odoo addons directory.</li>
  <li>Restart the Odoo server.</li>
  <li>Install the module from the Odoo administration panel.</li>
</ol>

<h2>Usage</h2>

<ol>
  <li>open the local host or the server website </li>
  <li>the ip adress with the details regarding the locationn will be present</li>
  <li>Log in to the Odoo system with appropriate access rights.</li>
  <li>Navigate to the "Task Management" menu to access the tasks.</li>
  <li>Create new tasks, providing the necessary details such as name, description, deadline, and stage.</li>
  <li>Users belonging to the "Own Records" group can view and update their own task records.</li>
  <li>Users belonging to the "All Records" group have access to all task records and can modify them.</li>
  <li>To generate a task report, select the desired tasks and choose the print option.</li>
  <li>On the website, navigate to the "Task Management" menu to access tasks.</li>
  <li>Click on a specific task to view its detailed content.</li>
</ol>

<h2>Credits</h2>

<p>The "task_management" module is developed and maintained by Khalid Alabyad.</p>