import feffery_antd_components as fac

def create_sidebar():
    return  fac.AntdSider([
                    fac.AntdMenu(
                        id='menu',
                        menuItems=[
                            {'component':'Item', 'props':{'key':'Home', 'title':'Home', 'icon':'antd-home', 'href': '/Home',}},
                            {'component':'Item', 'props':{'key':'Summary', 'title':'Summary', 'icon':'antd-bar-chart', 'href': '/Summary',}},
                            {'component':'Item', 'props':{'key':'Setting', 'title':'Setting', 'icon':'antd-setting', 'href': '/Setting',}},
                            {'component':'Item', 'props':{'key':'WaferMap', 'title':'WaferMap', 'icon':'fc-mind-map', 'href': '/WaferMap',}},
                        ], 
                        mode='inline',
                        style={"height": "100%", "overflow": "hidden auto"},
                    ),
                ], 
                collapsible=True,
                collapsed=True,
                collapsedWidth=60,
                style={"backgroundColor": "rgb(240,242,245)"}
                )
