```html
<div id="alert-message" class="alert-hidden">Formulario enviado</div>
  <form action="https://jsonplaceholder.typicode.com/posts/1" method="put">
    <div class="form-container">
      <h3 class="d-flex"><label style="width: 300px;" for="title"
          class="title text-5 text-nowrap overflow-hidden">Hola</label></h3>
      <div>
        <input disabled name="title" type="text" placeholder="Type something..." />
        <div class="buttons d-flex mt-2" style="gap: 10px;">

        </div>
      </div>
      <div class="form-container">
        <h3 class="d-flex"><label style="width: 300px;" for="id"
            class="id text-5 text-nowrap overflow-hidden">Hola</label></h3>
        <div>
          <input disabled name="id" type="text" placeholder="Type something..." />
          <div class="buttons d-flex mt-2" style="gap: 10px;">

          </div>
        </div>
      </div>
      <div class="form-container">
        <h3 class="d-flex"><label style="width: 300px;" for="id"
            class="id text-5 text-nowrap overflow-hidden">Hola</label></h3>
        <div>
          <select disabled name="select" type="text" placeholder="Type something...">
            <option value="1">Option 1</option>
            <option value="2">Option 2</option>
            <option value="3">Option 3</option>
          </select>
          <div class="buttons d-flex mt-2" style="gap: 10px;">

          </div>
        </div>
      </div>
  </form>
  <style>
    body {
      background-color: #36d;
    }

    input,
    select {
      width: 100%;
      height: 3rem;
      font-size: 1.5rem;
      padding: 0.5rem;
      border-radius: 0.25rem;
      border: 1px solid #ccc;

      display: none;
    }

    #alert-message {
      position: fixed;
      top: 20px;
      right: 20px;
      background-color: #28a745;
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      opacity: 0;
      transition: opacity 0.5s ease;
      z-index: 1000;
      font-family: sans-serif;
    }

    #alert-message.alert-visible {
      opacity: 1;
    }

    #alert-message.alert-hidden {
      opacity: 0;
      pointer-events: none;
    }
  </style>
  <script type="module" src="/src/main.js"></script>
```
let currentEditing = null // Guarda el campo en edición actual

const createEditButton = () => {
  const button = document.createElement("button")
  button.innerHTML = `<i aria-hidden="true">E</i>`
  button.type = "button"
  button.classList.add("btn", "btn-primary", "edit-button")
  return button
}

const createSaveButton = () => {
  const button = document.createElement("button")
  button.textContent = "Aceptar"
  button.type = "submit"
  button.classList.add("btn", "btn-success", "w-50", "save-button")
  button.style.display = "none"
  return button
}

const createCancelButton = () => {
  const button = document.createElement("button")
  button.textContent = "Cancelar"
  button.type = "button"
  button.classList.add("btn", "btn-danger", "w-50", "cancel-button")
  button.style.display = "none"
  return button
}

const submitForm = () => {
  const form = document.querySelector("form")
  if (form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault()
      showAlert("Formulario enviado")
    })
  }
}

const showAlert = (message) => {
  const alertBox = document.getElementById("alert-message")
  if (!alertBox) return

  alertBox.textContent = message
  alertBox.classList.remove("alert-hidden")
  alertBox.classList.add("alert-visible")

  setTimeout(() => {
    alertBox.classList.remove("alert-visible")
    alertBox.classList.add("alert-hidden")
  }, 3000) // Oculta luego de 3 segundos
}

const cancelEditing = () => {
  if (currentEditing) {
    const {
      field,
      label,
      editButton,
      saveButton,
      cancelButton,
      originalValue,
    } = currentEditing
    field.disabled = true
    field.style.display = "none"
    field.value = originalValue // restaurar el valor original
    editButton.style.display = "inline-block"
    saveButton.style.display = "none"
    cancelButton.style.display = "none"
    currentEditing = null
  }
}

const init = () => {
  document.querySelectorAll(".form-container").forEach((div) => {
    const label = div.querySelector("label")
    const field = div.querySelector("input, select") // 👈 Detecta input o select
    const editButton = createEditButton()
    const buttonsContainer = div.querySelector(".buttons")
    const saveButton = createSaveButton()
    const cancelButton = createCancelButton()

    buttonsContainer.appendChild(saveButton)
    buttonsContainer.appendChild(cancelButton)

    label.after(editButton)

    editButton.addEventListener("click", () => {
      if (currentEditing) cancelEditing()

      const originalValue =
        field.tagName === "SELECT"
          ? [...field.options].find((o) => o.value === field.value)?.textContent
          : label.textContent

      field.value = label.textContent // para input o para select si coincide
      field.disabled = false
      field.focus()
      field.style.display = "inline-block"
      editButton.style.display = "none"
      saveButton.style.display = "inline-block"
      cancelButton.style.display = "inline-block"

      currentEditing = {
        field,
        label,
        editButton,
        saveButton,
        cancelButton,
        originalValue: label.textContent,
      }
    })

    saveButton.addEventListener("click", () => {
      if (field.value.trim() === "") {
        alert("El campo no puede estar vacío")
        return
      }

      // Actualizar label con texto visible (en caso de select, no el value)
      if (field.tagName === "SELECT") {
        const selectedOption = field.options[field.selectedIndex]
        label.textContent = selectedOption.textContent
      } else {
        label.textContent = field.value
      }

      field.disabled = true
      field.style.display = "none"
      editButton.style.display = "inline-block"
      saveButton.style.display = "none"
      cancelButton.style.display = "none"
      currentEditing = null
      submitForm()
    })

    cancelButton.addEventListener("click", () => {
      cancelEditing()
    })
  })
}

init()

```js

```
