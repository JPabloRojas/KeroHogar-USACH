# API

## Formato

Las llamadas de API contienen el formato estandard de REST, siendo de siguiente manera:

```HOST/version/ENTIDAD/IDRECURSO ``` 

Siendo ENTIDAD el nombre del modelo o elemento solicitado EN INGLES y en PLURAL (ej: clients, products). En el caso de necesitar un registro en particular, se usa IDRECURSO, que es el id del recurso a minupular.

El método de solicitud (GET, POST, PUT, etc) dependerá de la acción. Se establecen las acciones en la siguiente lista:

### Llamadas a Entidad (```HOST/version/ENTIDAD```)
 - GET: Obtiene todas las entidades
 - POST: Crea un nuevo objeto de la entidad requerida
 - PUT: NO PERMITIDO
 - DELETE: Borrar todo

### Llamadas a Instancia (```HOST/version/ENTIDAD/IDRECURSO```)
 - GET: Obtiene la entidad especificada, con id IDRECURSO
 - POST: NO PERMITIDO
 - PUT: Edita la entidad especificada
 - DELETE: Elimina la entidad especificada

### Llamadas a Atributos de Entidad (```HOST/version/ENTIDAD/IDRECURSO/NOMBREATTR```)
 - GET: Obtiene todas los atributos posibles de tipo NOMBREATTR de la entidad IDRECURSO
 - POST: Crea un nuevo objeto de la entidad requerida de tipo NOMBREATTR
 - PUT: NO PERMITIDO
 - DELETE: Borrar todos los atributos tipo NOMBREATTR de la entidad IDRECURSO

### Llamadas a atributos específicos de Instancia (```HOST/version/ENTIDAD/IDRECURSO/NOMBRE_ATTR/IDATTR```)
 - GET: Obtiene el valor del atributo IDATTR de tipo NOMBRE_ATTR en la entidad especificada con IDRECURSO
 - POST: NO PERMITIDO
 - PUT: Edita el atributo especificado (IDATTR) de la entidad especificada (IDRECURSO)
 - DELETE: Elimina el atributo especificado (IDATTR) de la entidad especificada (IDRECURSO)
 
## Casos borde y retornos generalizados

En el caso de que la solicitud esté dirigida a una entidad que no tenga sentido en el negocio, la misma no estará disponible, retornando un estado HTTP ```403 FORBIDDEN```. Ahora, si es a una entidad que si tiene sentido, más el método NO está permitido, se enviará una respuesta ```405 METHOD NOT ALLOWED``` (ej: Delete a una dirección tipo ```HOST/version/ENTIDAD```). En el caso de malformación o error de sintaxis, se enviará un error ```400 BAD REQUEST``` 


## Esqueletos de Solicitud

### Producto

#### Obtener todos los productos:

> Parámetro: Ninguno
> Método: GET
> Ruta: ```HOST/version/products/```

Resultado: 
```javascript
[
    {
        id: 1,
        name: "Producto",
        price: 321,
        has_formats: true
    },
    {
        id: 2,
        name: "Producto 2",
        price: 123,
        has_formats: false
    }
]
```

#### Obtener cierto producto:

> Parámetro: id de producto 
> Ruta: ```HOST/version/products/ID```
> Método: GET

Resultado: 
```javascript
{
    name: "Producto",
    price: "Precio",
    has_formats: true/false
}
```

### Formatos

#### Obtener todos los formatos para cierto producto:

> Parámetro: id del producto
> Ruta: ```HOST/version/products/ID/formats``` (ejemplo producto 1)
> Método: GET

Resultado: 
```javascript
[
    {
        id: 1,
        name: "bidon chico",
        capacity: 10,
        added_price: 2,
        minimum_quantity: 10
    },
    {
        id: 5,
        name: "bidon grande",
        capacity: 50,
        added_price: 7,
        minimum_quantity: 30
    }
]
```

##### Obtener cierto formato de cierto producto:

> Parámetro: ID de producto e ID formato
> Ruta: ```HOST/version/product/ID/formats/IDFORMAT```
> Método: GET

Resultado: 
```javascript
{
    name: "Producto",
    price: "Precio"
    has_formats: true/false
}
```

#### Obtener descuentos de cierto producto:

> Parámetro: ID de producto (URL)
> Ruta: ```HOST/version/product/ID/discounts```
> Método: GET

Resultado: 
```javascript
[
    {
        id: 1,
        discount_per_liter: 3,
        min_qty: 2,
        max_qty: 4,
    },
    {
        id: 2,
        discount_per_liter: 4,
        min_qty: 6,
        max_qty: 12,
    }
]
```

### Direcciones (VER EXPLICACIÓN!)

Explicación: La idea es verificar esto usando el token de sesión. Como no está implementado, se aceptará el consultar como el resto de las entidades sin verificación. Si la autentificación no corresponde, se retornará un estado ```401 Unauthorized```

#### Obtener todas lss direcciones de cierto usuario:

> Parámetro: ID USUARIO
> Método: GET
> Ruta: ```HOST/version/users/IDUSER/addresses```


Resultado: 
```javascript
[
    {
        id: 1,
        town: "Vitacura",
        addr: "Av. Siempre Muerta 54362",
        alias: "Casa vieja"
    },
    {
        id: 6,
        town: "Las Condes",
        addr: "Malta 762",
        alias: "Casa Mamá"
    }
]
```

#### Crear nueva dirección relacionada con el usuario:

> Parámetro: ID USUARIO (URL) y datos de la dirección (Body)
> Método: POST
> Ruta: ```HOST/version/users/IDUSER/addresses```

Body: 
```javascript
{
    townID: 1
    addr: "Av. Pol McCarne 1212",
    alias: "Estudio"
}
```

Resultado: ```HTTP 201 CREATED```

#### Editar nueva dirección relacionada con el usuario:

> Parámetro: ID USUARIO (URL), ID de dirección (URL) y datos de la dirección (Body)
> Método: PUT
> Ruta: ```HOST/version/users/IDUSER/addresses/ADDRID```

Resultado: 
```javascript
{
    townID: 3
    addr: "Av. Veganos 421",
    alias: "Estudio fotográfico"
}
```

Resultado: ```HTTP 200 OK```


#### Borrar una dirección relacionada con el usuario:

> Parámetro: ID USUARIO (URL), ID de dirección (URL)
> Método: DELETE
> Ruta: ```HOST/version/users/IDUSER/addresses/ADDRID```

Resultado: ```HTTP 200 OK```

### Descuentos

#### Obtener todos los descuentos

> Parámetro: Ninguno
> Método: GET
> Ruta: ```HOST/version/discounts/```

Resultado:

```javascript
[
    {
        id: 1,
        discount_per_liter: 3,
        min_qty: 2,
        max_qty: 4,
        product_id: 2
    },
    {
        id: 2,
        discount_per_liter: 4,
        min_qty: 6,
        max_qty: 12,
        product_id: 1
    }
]
```

#### Obtener a que productos se aplica cierto descuento

> Parámetro: Id Descuento (URL)
> Método: GET
> Ruta: ```HOST/version/discounts/IDDESCUENTO```

Resultado:

```javascript
[
    {
        id: 1,
        name: "Producto",
        price: 321,
        has_formats: true
    }
]
```

### Pedido/Orden

#### Obtener todos los pedidos de un usuario
> Parámetro: Ninguno
> Método: GET
> Ruta: ```HOST/version/clients/IDClient/orders```

Resultado:

```javascript
[
   {
        id: 1,
        delivery_status: 1,
        payment_status: 2,
        amount: 14230,
        delivery_date: 2019-07-29,
   },
   {
        id: 4
        delivery_status: 1,
        payment_status: 2,
        amount: 14230,
        delivery_date: 2019-07-29,
   }
]
```

#### Obtener detalle de una orden específica
> Parámetro: IDCliente (URL) y IDOrden (URL)
> Método: GET
> Ruta: ```HOST/version/clients/IDClient/orders/IDOrden```

Resultado:
```javascript
 {
    id: 1,
    address:{
        id: 1,
        town: "Vitacura",
        addr: "Av. Siempre Muerta 54362",
        alias: "Casa vieja"
    },
    delivery_status: 1,
    payment_status: 2,
    amount: 14230,
    delivery_date: 2019-07-29,
    products:[
        {
            id: 1,
            qty: 23,
            formatID: 1
        }
    ],
    time_blocks:[
    {
        start: "10:00",
        end: "11:00"
    },
    {
        start: "14:00",
        end: "16:00"
    }
    ]
}
```

#### Crear/Ingresar nueva orden

> Parámetro: IDCliente (URL) e información de pedido (Body)
> Método: POST
> Ruta: ```HOST/version/clients/IDClient/orders```

Body:
```javascript
{
    addressID: 1,
    amount: 12391,
    delivery_date: 2018-12-28,
    time_block:[
    {
        id: 3
    },
    {
        id:2
    }],
    products:[
    {
        id:1,
        format:2,
        quantity:32
    }]
}
```

Resultado: ```HTTP 201 CREATED```


### Bloques de tiempo
Obtener los bloques de tiempo disponibles

> Parámetro: Estado (available en la ruta)
> Método: GET
> Ruta: ```HOST/version/timeblocks/available```


Resultado:
```javascript
[
    {
    "start":"9:00",
    "end": "10:00"
    }
]

```

