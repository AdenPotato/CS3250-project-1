---
name: uml
description: Write or refresh the PlantUML use case and class diagrams in uml/ from the design docs and the actual models, then render them. Use in the Modeling phase and whenever the model changes.
---

# /uml

Generate `uml/use_case.wsd` and `uml/class.wsd`. Worth 5 rubric points each, and both are presented at the checkpoint. Both ship as empty stubs.

Take which one as an argument (`/uml class`); with none, do both.

## Sources

- **Class diagram**: `src/app/models.py` is the truth, [data_model.md](../../../docs/design/data_model.md) is the explanation. Read the code - a diagram drawn from the doc alone drifts.
- **Use case diagram**: [use_cases.md](../../../docs/design/use_cases.md), cross-checked against the routes actually in `src/app/routes.py`.

## Class diagram

`uml/class.wsd` needs three classes with their attributes and types, both relationships with multiplicities, and `Enrollment` marked as the association class.

```plantuml
@startuml class
left to right direction
hide circle

class User {
  +id : String <<PK>>
  +name : String
  +about : String
  +passwd : LargeBinary
}

class Course {
  +prefix : String <<PK>>
  +number : String <<PK>>
  +name : String
  +credits : Integer
}

class Enrollment {
  +user_id : String <<PK,FK>>
  +course_prefix : String <<PK,FK>>
  +course_number : String <<PK,FK>>
  +grade : String
}

User "1" -- "0..*" Enrollment
Course "1" -- "0..*" Enrollment
note on link : association class -\ncarries the grade
@enduml
```

Points to get right: the **composite primary key** on `Course`, the composite FK from `Enrollment`, and the fact that `Enrollment` resolves a many-to-many because it carries an attribute. That last point is what the diagram is being graded for.

## Use case diagram

`uml/use_case.wsd` needs both actors, the eight use cases, a system boundary, and the two relationships.

```plantuml
@startuml use_case
left to right direction

actor Visitor
actor Student

rectangle "GPA Calculator" {
  usecase UC1 as "Sign up"
  usecase UC2 as "Sign in"
  usecase UC3 as "Sign out"
  usecase UC4 as "View enrollments"
  usecase UC5 as "View GPA"
  usecase UC6 as "Record an enrollment"
  usecase UC7 as "Update a grade"
  usecase UC8 as "Delete an enrollment"
}

Visitor --> UC1
Visitor --> UC2
Student --> UC3
Student --> UC4
Student --> UC6
Student --> UC8

UC4 ..> UC5 : <<include>>
UC7 ..> UC6 : <<extend>>
@enduml
```

`Student` inheriting from `Visitor` is a reasonable refinement if the team wants it. Keep `left to right direction` - the default layout is unreadable past four use cases.

## Render and commit

```
plantuml uml/class.wsd uml/use_case.wsd
```

Or the PlantUML extension in VS Code. **Commit the rendered PNGs beside the sources** - the instructor should not have to render them, and the checkpoint is presented from images.

## Keep them true

A diagram that disagrees with the code is worth less than one that is plainly incomplete. Re-run this after any `/new-model`, and check the use case diagram against `routes.py` before the checkpoint.
