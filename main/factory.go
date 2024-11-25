components {
  id: "factory"
  component: "/main/factoryWS.script"
}
embedded_components {
  id: "koi_factory"
  type: "factory"
  data: "prototype: \"/main/koi.go\"\n"
  ""
}
embedded_components {
  id: "rtt"
  type: "label"
  data: "size {\n"
  "  x: 128.0\n"
  "  y: 32.0\n"
  "}\n"
  "text: \"Label\"\n"
  "font: \"/builtins/fonts/default.font\"\n"
  "material: \"/builtins/fonts/label-df.material\"\n"
  ""
  position {
    x: 180.0
    y: 320.0
  }
}
embedded_components {
  id: "id"
  type: "label"
  data: "size {\n"
  "  x: 128.0\n"
  "  y: 32.0\n"
  "}\n"
  "text: \"Label\"\n"
  "font: \"/builtins/fonts/default.font\"\n"
  "material: \"/builtins/fonts/label-df.material\"\n"
  ""
  position {
    x: 180.0
    y: 300.0
  }
}
embedded_components {
  id: "target"
  type: "label"
  data: "size {\n"
  "  x: 128.0\n"
  "  y: 32.0\n"
  "}\n"
  "text: \"Label\"\n"
  "font: \"/builtins/fonts/default.font\"\n"
  "material: \"/builtins/fonts/label-df.material\"\n"
  ""
  position {
    x: 180.0
    y: 280.0
  }
}
