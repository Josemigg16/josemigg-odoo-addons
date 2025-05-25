# Example

```xml
<t t-name="prueba">
    <t t-foreach="docs" t-as="o">
        <main class="main-container" style="margin-top: 20px; font-family: Arial;">
                <h1>HOLÁ</h1>
                <t t-set="base_url" t-value="request.httprequest.url_root"/>
                   <base t-att-href="base_url"/>
                   <meta charset="utf-8" />
                    <img t-att-src="'data:image/png;base64,%s' %  o.partner_id.image_1920.decode('utf-8')" style="height: 100px; width: 100px;"/>



                <div style="display: flex;">
                    <div style="background: red; width: 100px;">
                        a
                    </div>
                    <div style="background: blue; width: 100px;">
                        b
                    </div>
                </div>
        </main>
    </t>
</t>
```
