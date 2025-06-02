/** @odoo-module */

import { Component, onWillStart, useState } from "@odoo/owl"
import { useService } from "@web/core/utils/hooks"
import { registry } from "@web/core/registry"

export class ChildComponent extends Component {
  static template = "custom_owl_components.ChildComponent"
  setup() {
    this.state = useState({ employee_id: 0 })
    this.rpc = useService("rpc")
    onWillStart(async () => {
      let user = await this.rpc("/my/user-info")
      this.state.employee_id = user.employee_id
    })
  }

  onSubmit(e) {
    e.preventDefault()

    const form = e.currentTarget
    this.submitForm(form)
  }

  onSelectChange(e) {
    const form = e.currentTarget.closest("form")
    this.submitForm(form)
  }

  submitForm(form) {
    const formData = new FormData(form)
    const actionUrl = form.action // 👈 Aquí obtienes el `action`

    fetch(actionUrl, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) throw new Error("Network error")
        return response.json()
      })
      .then((data) => {
        console.log("Success:", data)
      })
      .catch((error) => {
        console.error("Error:", error)
      })
  }
}

export class ExampleComponent extends Component {
  static template = "custom_owl_components.ExampleComponent"
  static components = { ChildComponent }

  setup() {
    this.state = useState({ user: {}, employee: {}, countries: [] })
    this.orm = useService("orm")
    this.rpc = useService("rpc")
    onWillStart(async () => {
      let user = await this.rpc("/my/user-info")
      console.log("user:", user)

      this.state.user = await this.orm.searchRead("res.users", [
        ["id", "=", user.id],
      ])
      this.state.employee = await this.orm.searchRead("hr.employee", [
        ["user_id", "=", user.id],
      ])
      this.state.countries = await this.orm.searchRead(
        "res.country",
        [],
        ["name"]
      )

      console.log("USUARIO:", this.state.user)
      console.log("empleado:", this.state.employee)
      console.log("countries:", this.state.countries)
    })
  }
}

registry
  .category("public_components")
  .add("custom_owl_components.ExampleComponent", ExampleComponent)
  .add("custom_owl_components.ChildComponent", ChildComponent)
