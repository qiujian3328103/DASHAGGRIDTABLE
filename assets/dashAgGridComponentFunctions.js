var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.EditDeleteButton = function (props) {
    const { setData, data } = props;

    function onEditClick() {
        setData({ action: 'edit', rowId: data.Id });
    }

    function onDeleteClick() {
        setData({ action: 'delete', rowId: data.Id });
    }

    function onViewClick() {
        setData({ action: 'view', rowId: data.Id });
    }

    return React.createElement(
        'div',
        { style: { display: 'flex', justifyContent: 'space-evenly', alignItems: 'center' } },
        React.createElement(
            'button',
            {
                onClick: onEditClick,
                className: 'edit-btn rounded-full p-[10px] text-md text-white cursor-pointer hover:bg-lightblue-600',
            },
            'Edit'
        ),
        React.createElement(
            'button',
            {
                onClick: onDeleteClick,
                className: 'delete-btn rounded-full p-[10px] text-md text-white cursor-pointer hover:bg-lightred-600',
            },
            'Delete'
        ),
        React.createElement(
            'button',
            {
                onClick: onViewClick,
                className: 'view-btn rounded-full p-[10px] text-md text-white cursor-pointer hover:bg-lightgreen-600',
            },
            'View'
        )
    );
};
