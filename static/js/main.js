(function (){
    window.addEventListener('load', function () {
        const currentHeight = window.sessionStorage.getItem('currentHeight')
        window.scroll(0, parseInt(currentHeight))
        const input = document.getElementsByTagName('input')
        for (let item of input){
            item.autocomplete = 'off'
        }
        const pages = document.getElementsByClassName('aItem')
        const currentRoute = window.location.pathname
        for (let item of pages){
            const currentPathName = '/'+item.href.split('/')[3]
            if (currentRoute === currentPathName){
                item.className = 'aItem active'
            }
        }
    })

    const aItem = document.getElementsByTagName('a')
    for (let item of aItem){
        item.addEventListener('click', function (){
            for( let i of aItem){
                i.className = 'aItem'
            }
            this.className = 'active aItem'
            window.sessionStorage.setItem('currentHeight', 0)
        })
    }

    const showDialog = document.getElementsByClassName('showDialog')[0]
    const createDialog = document.getElementsByClassName('createMomentDialog')[0]
    const closeDialog = document.getElementsByClassName('closeDialogBox')[0]
    dialog(createDialog, showDialog, closeDialog)

    const goTop = document.getElementsByClassName('goTop')[0]
    const contentRight = document.getElementsByClassName('contentRight')[0]
    let currentHeight = 0;
    window.addEventListener('scroll', function (){
        currentHeight = this.scrollY
        goTop.style.display = currentHeight > 300 ? 'block' : 'none'
        if (currentHeight >= 52) {
            contentRight.style.position = 'fixed'
            contentRight.style.top = '8px';
        }else {
            contentRight.style.position = 'absolute'
            contentRight.style.top = '60px';
        }
    })
    goTop.addEventListener('click', function (){
        window.scrollTo(0, 0)
    })

    const cover = document.getElementsByClassName('cover')[0]
    const editUserDialog = document.getElementsByClassName('editUserDialog')[0]
    const closeEditDialog = document.getElementsByClassName('closeDialogBox')[1]
    const editUserBtn = document.getElementsByClassName('editUserBtn')[0]
    dialog(editUserDialog, editUserBtn, closeEditDialog)

    function dialog(form, show, close){
        show.addEventListener('click', function (){
            form.style.display = 'block'
            cover.style.display = 'block'
        })
        close.addEventListener('click', function (){
            form.style.display = 'none'
            cover.style.display = 'none'
        })
    }

    const closeAvatarDialog = document.getElementsByClassName('closeAvatarDialog')[0]
    const showChangeAvatarDialogBtn = document.getElementsByClassName('changeAvatar')[0]
    const editAvatarDialog = document.getElementsByClassName('editAvatarDialog')[0]
    dialog(editAvatarDialog, showChangeAvatarDialogBtn, closeAvatarDialog)

    //发布评论
    const addCommentBtn = document.getElementsByClassName('addCommentBtn')
    const addCommentInput = document.getElementsByClassName('addCommentInput')
    submitComment(addCommentInput, addCommentBtn, showBtn, hiddenBtn)
    function showBtn(i){
        addCommentBtn[i].style.display = 'block'
        addCommentInput[i].style.width = '570px'
    }
    function hiddenBtn(i){
        addCommentBtn[i].style.display = 'none'
        addCommentInput[i].style.width = '631px'
    }

    //控制input样式
    function submitComment(input, btn, showBtn, hiddenBtn){
        const inputContent = Array(input.length).fill('')
        for (let i = 0; i < input.length; i++){
            const _input = input[i]
            const _btn = btn[i]
            _btn.addEventListener('click', function (){
                window.sessionStorage.setItem('currentHeight', currentHeight)
            })
            _input.addEventListener('click', () => showBtn(i))
            _input.addEventListener('input', function (){
                inputContent[i] = this.value
                this.value.length > 0 ? showBtn(i) : hiddenBtn(i)
            })
            _input.addEventListener('blur', function (){
                (inputContent[i] === undefined || inputContent[i] === '') && hiddenBtn(i)
            })
        }
    }

    //控制input显示隐藏
    const showComments = document.getElementsByClassName('showComments')
    const commentList = document.getElementsByClassName('commentList')
    controlInput(showComments,commentList, '收起评论', '查看评论')

    //控制input显示隐藏
    const replyCommentBtn = document.getElementsByClassName('replyCommentBtn')
    const replyCommentInput = document.getElementsByClassName('replyCommentInput')
    controlInput1(replyCommentBtn,replyCommentInput, '收起回复', '回复')
    function controlInput(btn, input, afterText, beforeText){
        const flag = Array(btn.length).fill(false)
        for (let i = 0; i < btn.length; i++){
            btn[i].addEventListener('click', function (){
                flag[i] = !flag[i]
                input[i].style.display = flag[i] ? 'block' : 'none'
                btn[i].innerHTML = flag[i] ? afterText : `${beforeText}(${btn[i].tabIndex})`
            })
        }
    }
    function controlInput1(btn, input, afterText, beforeText){
        const flag = Array(btn.length).fill(false)
        for (let i = 0; i < btn.length; i++){
            btn[i].addEventListener('click', function (){
                flag[i] = !flag[i]
                input[i].style.display = flag[i] ? 'block' : 'none'
                btn[i].innerHTML = flag[i] ? afterText : beforeText
            })
        }
    }

    //回复评论
    const replyCommentBtnSub = document.getElementsByClassName('replyCommentBtnSub')
    submitComment(replyCommentInput, replyCommentBtnSub, showBtnReply, hiddenReply)
    function showBtnReply(i){
        replyCommentBtnSub[i].style.display = 'block'
        replyCommentInput[i].style.width = '517px'
    }
    function hiddenReply(i){
        replyCommentBtnSub[i].style.display = 'none'
        replyCommentInput[i].style.width = '580px'
    }

    //删除评论
    const delComment = document.getElementsByClassName('delComment')
    for (let i = 0; i< delComment.length; i++){
        delComment[i].addEventListener('click', function (e){
            e.preventDefault()
            if(confirm("确定要删除该评论吗？删除将不能恢复！")){
                window.sessionStorage.setItem('currentHeight', currentHeight)
                document.getElementsByClassName('delForm')[i].submit()
            }
        })
    }

    //点击图片定向到上传头像
    const editAvatar = document.getElementsByClassName('editAvatar')[0]
    const editUserAvatar = document.getElementsByClassName('editUserAvatar')[0]
    editUserAvatar.addEventListener('click', function (){
        editAvatar.click()
    })
})()